frappe.ui.form.on("SEI Import Batch", {
  refresh(frm) {
    if (!frm.is_new() && frm.doc.status !== "Cancelled") {
      if (!["Import Complete", "Import Complete with Errors"].includes(frm.doc.status)) {
        frm.add_custom_button(__("Dry Run Import"), () => {
          frappe.call({
            method: "sales_engagement_intelligence.sales_engagement_and_intelligence.api.run_import_batch",
            args: { batch: frm.doc.name, dry_run: 1 },
            freeze: true,
            freeze_message: __("Running dry run..."),
            callback: (r) => show_api_result_and_reload(frm, r),
          });
        });
      }

      frm.add_custom_button(__("Run Import"), () => {
        frappe.confirm(__("Run this import and create or update SEI records?"), () => {
          frappe.call({
            method: "sales_engagement_intelligence.sales_engagement_and_intelligence.api.run_import_batch",
            args: { batch: frm.doc.name, dry_run: 0 },
            freeze: true,
            freeze_message: __("Running import..."),
            callback: (r) => show_api_result_and_reload(frm, r),
          });
        });
      });
    }

    frm.add_custom_button(__("Download Template"), () => {
      frappe.set_route("List", "File", { file_url: ["like", "%docs/import_templates%"] });
      frappe.show_alert({ message: __('Templates are committed under docs/import_templates in the app repository.'), indicator: 'blue' });
    });

    if (!frm.is_new() && ["Draft", "Failed"].includes(frm.doc.status)) {
      frm.add_custom_button(__("Cancel Batch"), () => {
        frappe.call({
          method: "sales_engagement_intelligence.sales_engagement_and_intelligence.api.cancel_import_batch",
          args: { batch: frm.doc.name },
          callback: (r) => show_api_result_and_reload(frm, r),
        });
      });
    }

    if (!frm.is_new() && ["Dry Run Complete", "Import Complete", "Import Complete with Errors", "Failed"].includes(frm.doc.status)) {
      frm.add_custom_button(__("Reset to Draft"), () => {
        frappe.confirm(__("Reset this import batch to Draft? This does not undo created SEI records."), () => {
          frappe.call({
            method: "sales_engagement_intelligence.sales_engagement_and_intelligence.api.reset_import_batch_to_draft",
            args: { batch: frm.doc.name },
            callback: (r) => show_api_result_and_reload(frm, r),
          });
        });
      });
    }
  },
});


function show_api_result_and_reload(frm, r) {
  const message = (r && r.message) || null;
  if (message && message.ok === false) {
    frappe.show_alert({
      message: __('SEI import action failed. Review the batch details.'),
      indicator: 'red',
    }, 7);
  }
  frm.reload_doc();
}
