frappe.query_reports["Asset Usage and Outcomes"] = {
  filters: [
    {
      fieldname: "sei_thesis",
      label: __("Related Thesis"),
      fieldtype: "Link",
      options: "SEI Thesis"
    },
    {
      fieldname: "asset_type",
      label: __("Asset Type"),
      fieldtype: "Select",
      options: "\nHomepage\nService Page\nDiagnostic Offer\nCase Study\nTechnical Teardown\nTechnical Audit Sample\nDirectory Profile\nQuote Process Page\nOther"
    },
  ],
};
