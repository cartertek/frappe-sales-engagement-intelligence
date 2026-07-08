frappe.listview_settings['SEI Prospect'] = {
    add_fields: [
        'prospect_name',
        'prospect_type',
        'source_arena',
        'thesis',
        'qualification_status',
        'lifecycle_status',
        'ready_for_crm_conversion',
        'next_action_date',
        'crm_lead',
        'crm_deal',
        'assigned_to'
    ],
    get_indicator(doc) {
        const colors = {
            'Ready for CRM Conversion': 'green',
            'Qualified': 'green',
            'Find Contact': 'orange',
            'Research Complete': 'blue',
            'Needs Research': 'yellow',
            'Rejected': 'red',
            'Do Not Contact': 'red',
            'Converted to CRM Lead': 'gray',
            'Converted to CRM Deal': 'gray'
        };
        return [doc.lifecycle_status || doc.qualification_status, colors[doc.lifecycle_status] || 'gray', `lifecycle_status,=,${doc.lifecycle_status}`];
    }
};
