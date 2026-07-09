frappe.ui.form.on('SEI Prospect', {
    refresh(frm) {
        if (frm.is_new()) return;

        reload_if_cached_document_is_stale(frm);

        frm.add_custom_button(__('Recalculate Qualification'), () => {
            call_and_reload(frm, 'recalculate_qualification', { prospect: frm.doc.name });
        }, __('SEI Actions'));

        if (!is_terminal(frm)) {
            frm.add_custom_button(__('Apply Lifecycle Suggestion'), () => {
                call_and_reload(frm, 'apply_lifecycle_suggestion', { prospect: frm.doc.name });
            }, __('SEI Actions'));
        }

        if (['Qualified', 'Manually Approved'].includes(frm.doc.qualification_status)
            && !frm.doc.do_not_contact && !frm.doc.crm_lead) {
            frm.add_custom_button(__('Mark Ready for CRM Conversion'), () => {
                call_and_reload(frm, 'mark_ready_for_crm_conversion', { prospect: frm.doc.name });
            }, __('CRM Preparation'));
        }

        if (can_prepare_crm_lead(frm)) {
            frm.add_custom_button(__('Preview CRM Lead'), () => {
                frappe.call({
                    method: 'sales_engagement_intelligence.sales_engagement_and_intelligence.api.preview_crm_lead',
                    args: { prospect: frm.doc.name },
                    callback(r) {
                        const data = r.message || {};
                        const dialog = new frappe.ui.Dialog({
                            title: __('CRM Lead Preview'),
                            size: 'large',
                            fields: [
                                { fieldtype: 'HTML', fieldname: 'preview_html' }
                            ]
                        });
                        const eligibility = data.eligibility || {};
                        const reasons = (eligibility.reasons || []).map(reason => `<li>${frappe.utils.escape_html(reason)}</li>`).join('');
                        dialog.fields_dict.preview_html.$wrapper.html(`
                            <p><b>${__('Eligible')}:</b> ${eligibility.eligible ? __('Yes') : __('No')}</p>
                            ${reasons ? `<p><b>${__('Reasons')}</b></p><ul>${reasons}</ul>` : ''}
                            <pre style="white-space: pre-wrap; max-height: 420px; overflow: auto;">${frappe.utils.escape_html(JSON.stringify(data.payload || {}, null, 2))}</pre>
                        `);
                        dialog.show();
                    }
                });
            }, __('CRM Preparation'));

            if (is_manager_or_admin()) {
                frm.add_custom_button(__('Create CRM Lead'), () => {
                    frappe.confirm(
                        __('Create a CRM Lead from this SEI Prospect? Review the preview first if you have not already done so.'),
                        () => call_and_reload(frm, 'create_crm_lead', { prospect: frm.doc.name })
                    );
                }, __('CRM Preparation'));
            }
        }

        if (frm.doc.crm_lead || frm.doc.crm_deal) {
            frm.add_custom_button(__('Sync SEI Context to CRM'), () => {
                call_and_reload(frm, 'sync_sei_context_to_crm', { prospect: frm.doc.name });
            }, __('CRM Preparation'));
        }

        if (!['Converted to CRM Lead', 'Converted to CRM Deal', 'Do Not Contact'].includes(frm.doc.lifecycle_status)) {
            frm.add_custom_button(__('Mark Rejected'), () => {
                prompt_reason(__('Rejected Reason'), (reason) => {
                    call_and_reload(frm, 'mark_rejected', { prospect: frm.doc.name, reason });
                });
            }, __('SEI Actions'));
        }

        if (frm.doc.lifecycle_status !== 'Do Not Contact') {
            frm.add_custom_button(__('Mark Do Not Contact'), () => {
                frappe.confirm(__('Mark this prospect Do Not Contact? This blocks CRM preparation.'), () => {
                    prompt_reason(__('Reason'), (reason) => {
                        call_and_reload(frm, 'mark_do_not_contact', { prospect: frm.doc.name, reason });
                    });
                });
            }, __('SEI Actions'));
        }

        if (['Rejected', 'Do Not Contact'].includes(frm.doc.lifecycle_status)
            && is_manager_or_admin()) {
            frm.add_custom_button(__('Reopen Prospect'), () => {
                frappe.confirm(__('Reopen this protected prospect and recalculate qualification?'), () => {
                    call_and_reload(frm, 'reopen_prospect', { prospect: frm.doc.name });
                });
            }, __('SEI Actions'));
        }
    }
});


function reload_if_cached_document_is_stale(frm) {
    if (frm.__sei_freshness_check_in_progress || frm.__sei_reloading_stale_cache) return;
    if (!frm.doc?.name || !frm.doc?.modified) return;

    frm.__sei_freshness_check_in_progress = true;
    frm.disable_save();

    frappe.db.get_value('SEI Prospect', frm.doc.name, 'modified')
        .then((r) => {
            const server_modified = r?.message?.modified;
            if (!server_modified || !frm.doc?.modified) return;

            const local_time = frappe.datetime.str_to_obj(frm.doc.modified);
            const server_time = frappe.datetime.str_to_obj(server_modified);

            if (server_time > local_time) {
                frm.__sei_reloading_stale_cache = true;
                frappe.show_alert({
                    message: __('Reloading latest prospect version.'),
                    indicator: 'orange'
                });
                return frm.reload_doc();
            }
        })
        .finally(() => {
            frm.__sei_freshness_check_in_progress = false;
            frm.__sei_reloading_stale_cache = false;
            frm.enable_save();
        });
}

function can_prepare_crm_lead(frm) {
    return ['Qualified', 'Manually Approved'].includes(frm.doc.qualification_status)
        && !frm.doc.do_not_contact
        && !['Rejected', 'Do Not Contact'].includes(frm.doc.lifecycle_status)
        && !frm.doc.crm_lead;
}
function is_terminal(frm) {
    return ['Rejected', 'Do Not Contact', 'Converted to CRM Lead', 'Converted to CRM Deal'].includes(frm.doc.lifecycle_status);
}

function call_and_reload(frm, action, args) {
    frappe.call({
        method: `sales_engagement_intelligence.sales_engagement_and_intelligence.api.${action}`,
        args,
        freeze: true,
        callback(r) {
            if (r.message) {
                frappe.msgprint({
                    title: __('SEI Action Complete'),
                    message: `<pre style="white-space: pre-wrap;">${frappe.utils.escape_html(JSON.stringify(r.message, null, 2))}</pre>`,
                    indicator: 'green'
                });
            }
            frm.reload_doc();
        }
    });
}

function prompt_reason(label, callback) {
    frappe.prompt(
        [{ fieldtype: 'Small Text', fieldname: 'reason', label, reqd: 0 }],
        (values) => callback(values.reason),
        label
    );
}

function is_manager_or_admin() {
    return frappe.session.user === 'Administrator'
        || frappe.user_roles.includes('Administrator')
        || frappe.user_roles.includes('Sales Engagement Manager');
}
