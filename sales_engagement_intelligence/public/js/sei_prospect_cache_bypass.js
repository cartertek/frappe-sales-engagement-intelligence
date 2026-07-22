(() => {
    const VERSION = 'contact-placeholder-debug-20260721-1';
    const METHOD = 'sales_engagement_intelligence.sales_engagement_and_intelligence.api.log_contact_placeholder_debug';

    function safe(value) {
        try { return JSON.parse(JSON.stringify(value)); }
        catch (error) { return { serialization_error: String(error) }; }
    }

    function send(stage, details = {}) {
        const payload = {
            version: VERSION,
            stage,
            route: window.frappe?.get_route?.() || null,
            href: window.location.href,
            details: safe(details),
        };
        console.info('[SEI contact debug]', payload);
        if (!window.frappe?.call) return;
        frappe.call({ method: METHOD, args: { payload: JSON.stringify(payload) }, silent: true });
    }

    function inspectOpenContact(reason) {
        const frm = window.cur_frm;
        const grid = frm?.fields_dict?.contacts?.grid;
        const openForm = grid?.open_grid_row;
        const row = openForm?.row?.doc;
        const control = openForm?.fields_dict?.signal_relevance;
        const input = control?.$input?.get?.(0)
            || openForm?.wrapper?.find?.('[data-fieldname="signal_relevance"] textarea, [data-fieldname="signal_relevance"] input')?.get?.(0);
        send('inspect-open-contact', {
            reason,
            prospect: frm?.doc?.name,
            role: row?.contact_role,
            row_name: row?.name,
            has_grid: Boolean(grid),
            has_open_form: Boolean(openForm),
            open_form_keys: openForm ? Object.keys(openForm).sort() : [],
            has_control: Boolean(control),
            control_placeholder: control?.df?.placeholder,
            dom_placeholder: input?.getAttribute?.('placeholder'),
            role_map: frm?.__sei_contact_role_requirements || null,
            controller_marker: window.__sei_prospect_controller_marker || null,
            doctype_cached: Boolean(window.locals?.DocType?.['SEI Prospect']),
            doctype_js_has_marker: Boolean(window.locals?.DocType?.['SEI Prospect']?.__js?.includes?.('SEI_PROSPECT_CONTROLLER_20260721')),
        });
    }

    function install() {
        if (!window.frappe || window.__sei_contact_debug_installed) return;
        window.__sei_contact_debug_installed = true;
        send('diagnostic-installed', {
            has_frappe_call: Boolean(frappe.call),
            doctype_cached: Boolean(window.locals?.DocType?.['SEI Prospect']),
        });

        const originalCall = frappe.call.bind(frappe);
        frappe.call = function patchedCall(options, ...rest) {
            const method = typeof options === 'string' ? options : options?.method;
            if (method?.includes?.('get_prospect_contact_role_requirements')) {
                send('role-api-call-start', { method, args: options?.args });
                const originalCallback = options.callback;
                options = { ...options, callback(response) {
                    send('role-api-call-response', { response });
                    return originalCallback?.(response);
                }};
            }
            return originalCall(options, ...rest);
        };

        const observer = new MutationObserver(() => {
            if (document.querySelector('.form-in-grid.grid-row-open, .grid-row-open .form-in-grid')) {
                window.setTimeout(() => inspectOpenContact('mutation'), 0);
                window.setTimeout(() => inspectOpenContact('mutation+250ms'), 250);
            }
        });
        observer.observe(document.body, { childList: true, subtree: true });

        document.addEventListener('click', event => {
            if (event.target.closest?.('.grid-row, .grid-static-col, .grid-row-check')) {
                window.setTimeout(() => inspectOpenContact('grid-click+100ms'), 100);
                window.setTimeout(() => inspectOpenContact('grid-click+500ms'), 500);
            }
        }, true);
    }

    install();
    document.addEventListener('DOMContentLoaded', install);
    window.setTimeout(install, 1000);
})();
