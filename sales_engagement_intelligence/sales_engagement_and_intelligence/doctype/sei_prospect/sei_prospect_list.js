frappe.listview_settings['SEI Prospect'] = {
    show_tags: true,
    add_fields: [
        'prospect_name',
        'prospect_type',
        'source_arena',
        'qualification_status',
        'lifecycle_status',
        'ready_for_crm_conversion',
        'next_action_date',
        'crm_lead',
        'crm_deal',
        '_user_tags'
    ],
    formatters: {
        qualification_status(value) {
            const color = value === 'Qualified' ? 'green' : 'gray';
            return `<span class="indicator-pill ${color}">${frappe.utils.escape_html(value || '')}</span>`;
        }
    },
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
        const status_field = doc.lifecycle_status ? 'lifecycle_status' : 'qualification_status';
        const status = doc[status_field];
        return [status, colors[status] || 'gray', `${status_field},=,${status}`];
    }
};

(() => {
    const original_setup_columns = frappe.views.ListView.prototype.setup_columns;

    frappe.views.ListView.prototype.setup_columns = function(fields_override = null) {
        original_setup_columns.call(this, fields_override);

        if (this.doctype !== 'SEI Prospect' || !Array.isArray(this.columns)) {
            return;
        }

        const tag_column_index = this.columns.findIndex((column) => column.type === 'Tag');
        if (tag_column_index === -1) {
            return;
        }

        const [tag_column] = this.columns.splice(tag_column_index, 1);
        const id_column_index = this.columns.findIndex((column) => column.df?.fieldname === 'name');

        if (id_column_index === -1) {
            this.columns.push(tag_column);
            return;
        }

        this.columns.splice(id_column_index, 0, tag_column);
    };
})();

