frappe.query_reports["Interaction Attribution Summary"] = {
  filters: [
    {
      fieldname: "interaction_type",
      label: __("Interaction Type"),
      fieldtype: "Select",
      options: "\nInitial Outreach\nFollow-Up\nReply\nReferral\nMeeting Scheduling\nPost-Meeting\nResearch Note\nOther"
    },
    {
      fieldname: "channel",
      label: __("Channel"),
      fieldtype: "Select",
      options: "\nEmail\nLinkedIn\nPhone\nContact Form\nCommunity DM\nIn-Person\nReferral Intro\nOther"
    },
    {
      fieldname: "response_category",
      label: __("Response Category"),
      fieldtype: "Select",
      options: "\nNo Response\nPositive\nInterested\nWrong Person\nNot Now\nAlready Solved\nNo Budget\nBad Fit\nUnsubscribe / Do Not Contact\nMeeting Booked\nConverted to Deal\nOther"
    },
    {
      fieldname: "sei_thesis",
      label: __("Thesis"),
      fieldtype: "Link",
      options: "SEI Thesis"
    },
    {
      fieldname: "sei_asset",
      label: __("Asset"),
      fieldtype: "Link",
      options: "SEI Asset"
    },
  ],
};
