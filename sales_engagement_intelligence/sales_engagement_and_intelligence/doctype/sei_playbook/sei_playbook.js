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
    },
});

async function render_signal_types(frm) {
    const field = frm.get_field('signal_types');
    if (!field || !field.$wrapper) {
        return;
    }
    if (frm.is_new()) {
        field.$wrapper.html(`<div class="text-muted">${__('Save the Playbook to manage assigned Signal Types.')}</div>`);
        return;
    }

    const rows = await frappe.db.get_list('SEI Signal Type', {
        filters: { playbook: frm.doc.name },
        fields: ['name', 'signal_type_name', 'category', 'research_arena', 'active'],
        order_by: 'signal_type_name asc',
        limit: 500,
    });

    const body = rows.map((row) => {
        const name = frappe.utils.escape_html(row.signal_type_name || row.name || '');
        const category = frappe.utils.escape_html(row.category || '');
        const arena = frappe.utils.escape_html(row.research_arena || '');
        const active = row.active ? __('Yes') : __('No');
        const encoded = encodeURIComponent(row.name);
        return `<tr data-signal-type="${encoded}">
            <td><a href="/app/sei-signal-type/${encoded}">${name}</a></td>
            <td>${category}</td>
            <td>${arena}</td>
            <td>${active}</td>
            <td class="text-nowrap">
                <button class="btn btn-xs btn-default sei-edit-signal-type" data-name="${encoded}">${__('Edit')}</button>
                <button class="btn btn-xs btn-default sei-move-signal-type" data-name="${encoded}">${__('Move')}</button>
            </td>
        </tr>`;
    }).join('');

    field.$wrapper.html(`<div class="mb-2">
        <button class="btn btn-xs btn-primary sei-add-signal-type">${__('Add / Move Existing')}</button>
        <button class="btn btn-xs btn-default sei-new-signal-type">${__('New Signal Type')}</button>
    </div>
    <div class="table-responsive">
        <table class="table table-bordered table-sm">
            <thead><tr>
                <th>${__('Signal Type')}</th>
                <th>${__('Category')}</th>
                <th>${__('Research Arena')}</th>
                <th>${__('Active')}</th>
                <th>${__('Actions')}</th>
            </tr></thead>
            <tbody>${body || `<tr><td colspan="5" class="text-muted">${__('No Signal Types are assigned to this Playbook.')}</td></tr>`}</tbody>
        </table>
    </div>`);

    field.$wrapper.find('.sei-add-signal-type').on('click', () => show_assign_signal_type_dialog(frm));
    field.$wrapper.find('.sei-new-signal-type').on('click', () => {
        frappe.new_doc('SEI Signal Type', { playbook: frm.doc.name });
    });
    field.$wrapper.find('.sei-edit-signal-type').on('click', (event) => {
        const name = decodeURIComponent($(event.currentTarget).data('name'));
        const row = rows.find((item) => item.name === name);
        if (row) show_edit_signal_type_dialog(frm, row);
    });
    field.$wrapper.find('.sei-move-signal-type').on('click', (event) => {
        const name = decodeURIComponent($(event.currentTarget).data('name'));
        show_move_signal_type_dialog(frm, name);
    });
}

function show_assign_signal_type_dialog(frm) {
    const dialog = new frappe.ui.Dialog({
        title: __('Add / Move Signal Type'),
        fields: [{
            fieldname: 'signal_type',
            label: __('Signal Type'),
            fieldtype: 'Link',
            options: 'SEI Signal Type',
            reqd: 1,
            get_query: () => ({ filters: { playbook: ['!=', frm.doc.name] } }),
        }],
        primary_action_label: __('Add to Playbook'),
        primary_action: async (values) => {
            await frappe.call({
                method: 'sales_engagement_intelligence.sales_engagement_and_intelligence.doctype.sei_playbook.sei_playbook.assign_signal_type',
                args: { playbook: frm.doc.name, signal_type: values.signal_type },
            });
            dialog.hide();
            await render_signal_types(frm);
        },
    });
    dialog.show();
}

function show_edit_signal_type_dialog(frm, row) {
    const allowed_arenas = (frm.doc.research_arenas || []).map((item) => item.research_arena).filter(Boolean);
    const dialog = new frappe.ui.Dialog({
        title: __('Edit Signal Type'),
        fields: [
            { fieldname: 'category', label: __('Category'), fieldtype: 'Link', options: 'SEI Signal Type Category', reqd: 1, default: row.category },
            {
                fieldname: 'research_arena', label: __('Research Arena'), fieldtype: 'Link', options: 'SEI Research Arena', reqd: 1,
                default: row.research_arena,
                get_query: () => allowed_arenas.length ? ({ filters: { name: ['in', allowed_arenas] } }) : ({}),
            },
            { fieldname: 'active', label: __('Active'), fieldtype: 'Check', default: row.active ? 1 : 0 },
        ],
        primary_action_label: __('Save'),
        primary_action: async (values) => {
            await frappe.call({
                method: 'sales_engagement_intelligence.sales_engagement_and_intelligence.doctype.sei_playbook.sei_playbook.update_signal_type_from_playbook',
                args: { playbook: frm.doc.name, signal_type: row.name, ...values },
            });
            dialog.hide();
            await render_signal_types(frm);
        },
    });
    dialog.show();
}

function show_move_signal_type_dialog(frm, signal_type) {
    const dialog = new frappe.ui.Dialog({
        title: __('Move Signal Type'),
        fields: [{
            fieldname: 'playbook',
            label: __('Playbook'),
            fieldtype: 'Link',
            options: 'SEI Playbook',
            reqd: 1,
            get_query: () => ({ filters: { name: ['!=', frm.doc.name] } }),
        }],
        primary_action_label: __('Move'),
        primary_action: async (values) => {
            await frappe.call({
                method: 'sales_engagement_intelligence.sales_engagement_and_intelligence.doctype.sei_playbook.sei_playbook.move_signal_type',
                args: { signal_type, from_playbook: frm.doc.name, to_playbook: values.playbook },
            });
            dialog.hide();
            await render_signal_types(frm);
        },
    });
    dialog.show();
}
