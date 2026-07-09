frappe.query_reports["Import Batch Summary"] = {
  filters: [
    {
      fieldname: "source_type",
      label: __("Source Type"),
      fieldtype: "Select",
      options: "\nManual CSV\nDirectory Research\nJob Board Research\nLaunch Source Research\nGitHub / Technical Distress Research\nCommunity Research\nAgency / Partner List\nProcurement Research\nOther"
    },
    {
      fieldname: "source_arena",
      label: __("Source Arena"),
      fieldtype: "Data"
    },
    {
      fieldname: "import_kind",
      label: __("Import Kind"),
      fieldtype: "Select",
      options: "\nCombined Prospect + Initial Signal\nProspect Only\nSignal Only"
    },
    {
      fieldname: "import_mode",
      label: __("Import Mode"),
      fieldtype: "Select",
      options: "\nCreate Only\nUpdate Existing\nCreate or Update"
    },
    {
      fieldname: "status",
      label: __("Status"),
      fieldtype: "Select",
      options: "\nDraft\nDry Run Complete\nImport Complete\nImport Complete with Errors\nFailed\nCancelled"
    },
  ],
};
