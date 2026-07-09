frappe.query_reports["Response Category by Thesis"] = {
  filters: [
    {
      fieldname: "sei_thesis",
      label: __("Thesis"),
      fieldtype: "Link",
      options: "SEI Thesis"
    },
    {
      fieldname: "channel",
      label: __("Channel"),
      fieldtype: "Select",
      options: "\nEmail\nLinkedIn\nPhone\nContact Form\nCommunity DM\nIn-Person\nReferral Intro\nOther"
    },
  ],
};
