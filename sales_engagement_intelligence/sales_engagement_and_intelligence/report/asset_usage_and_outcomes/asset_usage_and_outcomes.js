frappe.query_reports["Asset Usage and Outcomes"] = {
  filters: [
    {
      fieldname: "sei_playbook",
      label: __("Related Playbook"),
      fieldtype: "Link",
      options: "SEI Playbook"
    },
    {
      fieldname: "asset_type",
      label: __("Asset Type"),
      fieldtype: "Select",
      options: "\nHomepage\nService Page\nDiagnostic Offer\nCase Study\nTechnical Teardown\nTechnical Audit Sample\nDirectory Profile\nQuote Process Page\nOther"
    },
  ],
};
