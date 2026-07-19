frappe.ui.form.on('SEI Message Draft', {
  refresh(frm) {
    if (frm.doc.prospect) {
      frappe.call({method:'sales_engagement_intelligence.sales_engagement_and_intelligence.api.get_prospect_contact_options',args:{prospect:frm.doc.prospect},callback(r){frm.set_df_property('to_contact','options',(r.message&&r.message.data||[]).join('\n'));}});
    }
    if (!frm.is_new() && !frm.doc.sent) frm.add_custom_button(__('Mark as Sent'),()=>frappe.call({method:'sales_engagement_intelligence.sales_engagement_and_intelligence.api.mark_message_draft_sent',args:{draft:frm.doc.name},freeze:true,callback(){frm.reload_doc();}}));
  },
  prospect(frm){frm.trigger('refresh');}
});
