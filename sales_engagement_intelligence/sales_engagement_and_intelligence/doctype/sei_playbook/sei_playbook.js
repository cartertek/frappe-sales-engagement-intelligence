const COMPACT_PLAYBOOK_TEXT_FIELDS = [
    'description',
    'thesis',
    'typical_prospect_types',
    'qualifying_signal_guidance',
    'disqualifying_guidance',
    'follow_up_guidance',
    'notes',
];

frappe.ui.form.on('SEI Playbook', {
    refresh(frm) {
        COMPACT_PLAYBOOK_TEXT_FIELDS.forEach((fieldname) => {
            const field = frm.get_field(fieldname);
            if (field && field.$input) {
                field.$input.css({ height: '88px', 'min-height': '88px' });
            }
        });

        render_signal_types(frm);

        if (!frm.is_new()) {
            frm.add_custom_button(__('Manage Signal Types'), () => {
                frappe.set_route('List', 'SEI Signal Type', { playbook: frm.doc.name });
            });
        }
    },

    before_save(frm) {
    },
});

async function render_signal_types(frm) {
    const field = frm.get_field('signal_types');
    if (!field || !field.$wrapper) {
        return;
    }
    if (frm.is_new()) {
        field.$wrapper.html(`<div class="text-muted">${__('Save the Playbook to view assigned Signal Types.')}</div>`);
        return;
    }

    const rows = await frappe.db.get_list('SEI Signal Type', {
        filters: { playbook: frm.doc.name },
        fields: ['name', 'category', 'research_arena', 'active'],
        order_by: 'signal_type_name asc',
        limit: 500,
    });

    if (!rows.length) {
        field.$wrapper.html(`<div class="text-muted">${__('No Signal Types are assigned to this Playbook.')}</div>`);
        return;
    }

    const body = rows.map((row) => {
        const name = frappe.utils.escape_html(row.name || '');
        const category = frappe.utils.escape_html(row.category || '');
        const arena = frappe.utils.escape_html(row.research_arena || '');
        const active = row.active ? __('Yes') : __('No');
        const href = `/app/sei-signal-type/${encodeURIComponent(row.name)}`;
        return `<tr>
            <td><a href="${href}">${name}</a></td>
            <td>${category}</td>
            <td>${arena}</td>
            <td>${active}</td>
        </tr>`;
    }).join('');

    field.$wrapper.html(`<div class="table-responsive">
        <table class="table table-bordered table-sm">
            <thead><tr>
                <th>${__('Signal Type')}</th>
                <th>${__('Category')}</th>
                <th>${__('Research Arena')}</th>
                <th>${__('Active')}</th>
            </tr></thead>
            <tbody>${body}</tbody>
        </table>
    </div>`);
}
