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
        if (frm.doc.sei_playbook && !is_terminal(frm)) {
            frm.add_custom_button(__('Apply Playbook Defaults'), () => {
                frappe.confirm(__('Apply playbook defaults to blank fields only? Existing values will not be overwritten.'), () => {
                    call_and_reload(frm, 'apply_playbook_defaults', { prospect: frm.doc.name });
                });
            }, __('Outreach Drafting'));
        }

        frm.add_custom_button(__('Preview Message Draft'), () => {
            prompt_message_template(frm);
        }, __('Outreach Drafting'));


        frm.add_custom_button(__('Mark Ready for CRM Conversion'), () => {
            mark_ready_for_crm_conversion(frm);
        }, __('CRM Preparation'));

        if (can_prepare_crm(frm)) {
            frm.add_custom_button(__('Find CRM Duplicates'), () => show_conversion_preview(frm), __('CRM Preparation'));

            frm.add_custom_button(__('Preview CRM Conversion'), () => show_conversion_preview(frm), __('CRM Preparation'));

            if (is_manager_or_admin()) {
                if (!frm.doc.crm_lead) {
                    frm.add_custom_button(__('Create CRM Lead'), () => {
                        confirm_create(frm, 'CRM Lead', 'create_crm_lead');
                    }, __('CRM Preparation'));
                }

                frm.add_custom_button(__('Create CRM Organization'), () => {
                    confirm_create(frm, 'CRM Organization', 'create_or_link_crm_organization');
                }, __('CRM Preparation'));

                if (has_contact_path(frm)) {
                    frm.add_custom_button(__('Create CRM Contact'), () => {
                        confirm_create(frm, 'CRM Contact', 'create_or_link_crm_contact');
                    }, __('CRM Preparation'));
                }

                frm.add_custom_button(__('Create CRM Deal'), () => {
                    prompt_deal_options(frm);
                }, __('CRM Preparation'));

                add_link_button(frm, 'CRM Lead', 'crm_lead');
                add_link_button(frm, 'CRM Organization', 'crm_organization');
                add_link_button(frm, 'Contact', 'crm_contact');
                add_link_button(frm, 'CRM Deal', 'crm_deal');
            }
        }

        render_signals_embedded_list(frm);

        add_open_button(frm, 'CRM Lead', frm.doc.crm_lead);
        add_open_button(frm, 'CRM Deal', frm.doc.crm_deal);
        add_open_button(frm, 'CRM Organization', frm.doc.crm_organization);
        add_open_button(frm, 'Contact', frm.doc.crm_contact);

        if ((frm.doc.crm_lead || frm.doc.crm_deal || frm.doc.crm_organization || frm.doc.crm_contact)
            && is_manager_or_admin()) {
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
            const server_modified = r && r.message && r.message.modified;
            if (!server_modified || !frm.doc || !frm.doc.modified) return;

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
        .always(() => {
            frm.__sei_freshness_check_in_progress = false;
            frm.__sei_reloading_stale_cache = false;
            frm.enable_save();
        });
}

function can_prepare_crm(frm) {
    return ['Qualified', 'Manually Approved'].includes(frm.doc.qualification_status)
        && !frm.doc.do_not_contact
        && !['Rejected', 'Do Not Contact'].includes(frm.doc.lifecycle_status);
}

function has_contact_path(frm) {
    return Boolean(frm.doc.primary_contact_name || frm.doc.primary_contact_email || frm.doc.primary_contact_url);
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
            const message = unwrap_api_message(r);
            if (message) {
                frappe.msgprint({
                    title: message.ok === false ? __('SEI Action Failed') : __('SEI Action Complete'),
                    message: `<pre style="white-space: pre-wrap;">${frappe.utils.escape_html(JSON.stringify(message, null, 2))}</pre>`,
                    indicator: message.ok === false ? 'red' : 'green'
                });
            }
            frm.reload_doc();
        }
    });
}

function mark_ready_for_crm_conversion(frm) {
    frappe.call({
        method: 'sales_engagement_intelligence.sales_engagement_and_intelligence.api.mark_ready_for_crm_conversion',
        args: { prospect: frm.doc.name },
        freeze: true,
        callback(r) {
            const message = unwrap_api_message(r) || {};
            if (message.ok === false) {
                show_crm_readiness_checklist(message);
                return;
            }
            frappe.msgprint({
                title: __('SEI Action Complete'),
                message: __('Prospect marked ready for CRM conversion.'),
                indicator: 'green'
            });
            frm.reload_doc();
        }
    });
}

function show_crm_readiness_checklist(message) {
    const details = message.error && message.error.details ? message.error.details : {};
    const requirements = details.requirements || [];
    const rows = requirements.map((requirement) => {
        const met = Boolean(requirement.met);
        const icon = met ? '✓' : '✕';
        const color = met ? 'green' : 'red';
        return `
            <li style="margin-bottom: var(--margin-xs);">
                <span class="indicator-pill ${color}" style="margin-right: var(--margin-xs);">${icon}</span>
                ${frappe.utils.escape_html(requirement.label || '')}
            </li>
        `;
    }).join('');
    const fallback = frappe.utils.escape_html((message.error && message.error.message) || __('Requirements not met.'));

    frappe.msgprint({
        title: __('CRM Readiness Requirements'),
        message: `
            <p>${fallback}</p>
            <ul style="list-style: none; padding-left: 0; margin-bottom: 0;">${rows}</ul>
        `,
        indicator: 'red'
    });
}

function show_conversion_preview(frm) {
    frappe.call({
        method: 'sales_engagement_intelligence.sales_engagement_and_intelligence.api.preview_crm_conversion',
        args: { prospect: frm.doc.name },
        freeze: true,
        callback(r) {
            const data = unwrap_api_data(r);
            const dialog = new frappe.ui.Dialog({
                title: __('CRM Conversion Preview'),
                size: 'extra-large',
                fields: [{ fieldtype: 'HTML', fieldname: 'preview_html' }]
            });

            dialog.fields_dict.preview_html.$wrapper.html(render_preview_html(data));
            dialog.show();
        }
    });
}


function unwrap_api_message(r) {
    return (r && r.message) || null;
}

function unwrap_api_data(r) {
    const message = unwrap_api_message(r) || {};
    return message.ok === true ? (message.data || {}) : message;
}

function render_preview_html(data) {
    const eligibility = data.eligibility || {};
    const reasons = (eligibility.reasons || [])
        .map(reason => `<li>${frappe.utils.escape_html(reason)}</li>`)
        .join('');
    const duplicates = data.duplicates || {};
    const payloads = data.payloads || {};

    return `
        <p><b>${__('Lead Creation Eligible')}:</b> ${eligibility.eligible ? __('Yes') : __('No')}</p>
        ${reasons ? `<p><b>${__('Blocking / Warning Reasons')}</b></p><ul>${reasons}</ul>` : ''}
        <h4>${__('Possible CRM Duplicates')}</h4>
        ${render_duplicate_group(__('CRM Leads'), duplicates.crm_leads || [], 'CRM Lead')}
        ${render_duplicate_group(__('CRM Organizations'), duplicates.crm_organizations || [], 'CRM Organization')}
        ${render_duplicate_group(__('CRM Contacts'), duplicates.crm_contacts || [], 'Contact')}
        ${render_duplicate_group(__('CRM Deals'), duplicates.crm_deals || [], 'CRM Deal')}
        <h4>${__('Payload Preview')}</h4>
        <pre style="white-space: pre-wrap; max-height: 420px; overflow: auto;">${frappe.utils.escape_html(JSON.stringify(payloads, null, 2))}</pre>
    `;
}

function render_duplicate_group(label, rows, doctype) {
    if (!rows.length) {
        return `<p><b>${label}:</b> ${__('None found')}</p>`;
    }

    const items = rows.map(row => {
        const title = row.title || row.name;
        const reason = row.reason || '';
        const route_doctype = doctype.toLowerCase().replace(/ /g, '-');
        const route = `/app/${route_doctype}/${encodeURIComponent(row.name)}`;
        return `<li><a href="${route}">${frappe.utils.escape_html(title)}</a> — ${frappe.utils.escape_html(reason)}</li>`;
    }).join('');
    return `<p><b>${label}</b></p><ul>${items}</ul>`;
}

function confirm_create(frm, label, action, options = {}) {
    frappe.confirm(
        __(`Create ${label} from this SEI Prospect? Review CRM duplicates/preview first if you have not already done so.`),
        () => call_and_reload(frm, action, { prospect: frm.doc.name, options })
    );
}

function prompt_deal_options(frm) {
    frappe.prompt(
        [
            {
                fieldtype: 'Check',
                fieldname: 'manager_override',
                label: __('Manager override: commercial basis confirmed outside SEI attribution')
            },
            {
                fieldtype: 'Check',
                fieldname: 'allow_direct_deal',
                label: __('Allow direct Deal creation without linked CRM Lead'),
                default: frm.doc.crm_lead ? 0 : 1
            }
        ],
        (values) => {
            confirm_create(frm, 'CRM Deal', 'create_crm_deal', {
                manager_override: Boolean(values.manager_override),
                allow_direct_deal: Boolean(values.allow_direct_deal)
            });
        },
        __('CRM Deal Options')
    );
}

function add_link_button(frm, doctype, fieldname) {
    if (frm.doc[fieldname]) return;
    const label = __(`Link Existing ${doctype}`);
    frm.add_custom_button(label, () => {
        frappe.prompt(
            [{ fieldtype: 'Link', fieldname: 'record_name', label: doctype, options: doctype, reqd: 1 }],
            (values) => {
                call_and_reload(frm, 'link_existing_crm_record', {
                    prospect: frm.doc.name,
                    doctype,
                    record_name: values.record_name
                });
            },
            label
        );
    }, __('CRM Preparation'));
}

function add_open_button(frm, doctype, record_name) {
    if (!record_name) return;
    frm.add_custom_button(__(`Open ${doctype}`), () => {
        frappe.set_route('Form', doctype, record_name);
    }, __('CRM Records'));
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



function prompt_message_template(frm) {
    const fields = [
        {
            fieldname: 'template',
            label: __('Message Template'),
            fieldtype: 'Link',
            options: 'SEI Message Template',
            reqd: 1,
            get_query() {
                const filters = { active: 1 };
                if (frm.doc.sei_playbook) filters.playbook = frm.doc.sei_playbook;
                return { filters };
            }
        }
    ];

    const default_template = frm.doc.suggested_message_template || null;
    frappe.prompt(fields, (values) => {
        show_message_draft_preview(frm, values.template);
    }, __('Preview Message Draft'), __('Render Preview'));

    // frappe.prompt does not expose a stable direct default hook across Frappe
    // versions. Keep the suggested template visible on the form instead of
    // relying on undocumented dialog internals.
    if (default_template) {
        frappe.show_alert({
            message: __('Suggested template: {0}', [default_template]),
            indicator: 'blue'
        });
    }
}

function show_message_draft_preview(frm, template) {
    frappe.call({
        method: 'sales_engagement_intelligence.sales_engagement_and_intelligence.api.preview_message_draft',
        args: { prospect: frm.doc.name, template },
        freeze: true,
        callback(r) {
            const message = unwrap_api_message(r) || {};
            if (message.ok === false) {
                frappe.msgprint({
                    title: __('Draft Preview Failed'),
                    message: `<pre style="white-space: pre-wrap;">${frappe.utils.escape_html(JSON.stringify(message, null, 2))}</pre>`,
                    indicator: 'red'
                });
                return;
            }
            const data = message.data || {};
            const dialog = new frappe.ui.Dialog({
                title: __('Message Draft Preview'),
                size: 'extra-large',
                fields: [{ fieldtype: 'HTML', fieldname: 'draft_html' }]
            });
            dialog.fields_dict.draft_html.$wrapper.html(render_message_draft_html(data));
            dialog.show();
        }
    });
}

function render_message_draft_html(data) {
    const missing = data.missing_variables || [];
    const missing_html = missing.length
        ? `<p><b>${__('Missing Variables')}:</b> ${missing.map(value => frappe.utils.escape_html(value)).join(', ')}</p>`
        : `<p><b>${__('Missing Variables')}:</b> ${__('None')}</p>`;
    const safety = data.safety || {};
    return `
        <p><b>${__('Channel')}:</b> ${frappe.utils.escape_html(data.channel || '')}</p>
        ${missing_html}
        <h4>${__('Subject')}</h4>
        <pre style="white-space: pre-wrap;">${frappe.utils.escape_html(data.subject || '')}</pre>
        <h4>${__('Body')}</h4>
        <pre style="white-space: pre-wrap; max-height: 420px; overflow: auto;">${frappe.utils.escape_html(data.body || '')}</pre>
        <h4>${__('Safety')}</h4>
        <pre style="white-space: pre-wrap;">${frappe.utils.escape_html(JSON.stringify(safety, null, 2))}</pre>
        <p class="text-muted">${__('This preview does not send outreach, create a Communication, create CRM records, or change lifecycle status.')}</p>
    `;
}


function render_signals_embedded_list(frm) {
    const field = frm.fields_dict.signals_embedded_list;
    if (!field || !field.$wrapper) return;

    const wrapper = field.$wrapper;

    if (frm.is_new()) {
        wrapper.html(`<p class="text-muted">${__('Save this prospect before adding signals.')}</p>`);
        return;
    }

    wrapper.html(`<p class="text-muted">${__('Loading signals...')}</p>`);

    frappe.db.get_list('SEI Signal', {
        fields: [
            'name',
            'signal_type',
            'signal_strength',
            'evidence_basis',
            'exclude_from_qualification',
            'confidence',
            'source_date',
            'modified'
        ],
        filters: { prospect: frm.doc.name },
        order_by: 'source_date desc, modified desc',
        limit: 100
    }).then((signals) => {
        wrapper.html(render_signals_table(frm, signals || []));
        wrapper.find('[data-sei-action="new-signal"]').on('click', () => {
            frappe.new_doc('SEI Signal', {
                prospect: frm.doc.name,
                prospect_name: frm.doc.prospect_name
            });
        });
    }).catch(() => {
        wrapper.html(`<p class="text-muted">${__('Unable to load signals.')}</p>`);
    });
}

function render_signals_table(frm, signals) {
    const new_button = `
        <button class="btn btn-xs btn-default" data-sei-action="new-signal">
            ${__('New Signal')}
        </button>
    `;

    if (!signals.length) {
        return `
            <div class="sei-signals-embedded-list">
                <div class="flex justify-between align-center" style="margin-bottom: var(--margin-sm);">
                    <p class="text-muted" style="margin: 0;">${__('No signals recorded for this prospect yet.')}</p>
                    ${new_button}
                </div>
            </div>
        `;
    }

    const rows = signals.map((signal) => {
        const route = `/app/sei-signal/${encodeURIComponent(signal.name)}`;
        const excluded = signal.exclude_from_qualification ? __('Yes') : __('No');
        const confidence = signal.confidence === null || signal.confidence === undefined
            ? ''
            : `${flt(signal.confidence, 2)}%`;

        return `
            <tr>
                <td><a href="${route}">${frappe.utils.escape_html(signal.signal_type || signal.name)}</a></td>
                <td>${render_signal_badge(signal.signal_strength)}</td>
                <td>${frappe.utils.escape_html(signal.evidence_basis || '')}</td>
                <td>${excluded}</td>
                <td>${confidence}</td>
                <td>${frappe.utils.escape_html(signal.source_date || '')}</td>
            </tr>
        `;
    }).join('');

    return `
        <div class="sei-signals-embedded-list">
            <div class="flex justify-between align-center" style="margin-bottom: var(--margin-sm);">
                <p class="text-muted" style="margin: 0;">${__('Signals linked to this prospect')}</p>
                ${new_button}
            </div>
            <div class="table-responsive">
                <table class="table table-bordered table-hover">
                    <thead>
                        <tr>
                            <th>${__('Signal Type')}</th>
                            <th>${__('Strength')}</th>
                            <th>${__('Evidence')}</th>
                            <th>${__('Excluded')}</th>
                            <th>${__('Confidence')}</th>
                            <th>${__('Source Date')}</th>
                        </tr>
                    </thead>
                    <tbody>${rows}</tbody>
                </table>
            </div>
        </div>
    `;
}

function render_signal_badge(strength) {
    if (!strength) return '';
    const color = {
        Strong: 'green',
        Moderate: 'orange',
        Weak: 'gray'
    }[strength] || 'gray';
    return `<span class="indicator-pill ${color}">${frappe.utils.escape_html(strength)}</span>`;
}
