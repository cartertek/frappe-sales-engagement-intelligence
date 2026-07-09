(() => {
    const PATCH_FLAG = '__sei_prospect_with_doc_cache_bypass';

    function install_sei_prospect_cache_bypass() {
        if (!window.frappe?.model?.with_doc || frappe.model[PATCH_FLAG]) return;

        const original_with_doc = frappe.model.with_doc.bind(frappe.model);

        frappe.model.with_doc = function (doctype, name, callback) {
            const docname = name || doctype;

            if (doctype === 'SEI Prospect' && window.locals?.[doctype]?.[docname]) {
                console.info('[SEI] force server fetch for SEI Prospect', docname);
                frappe.model.remove_from_locals(doctype, docname);
            }

            return original_with_doc(doctype, name, callback);
        };

        frappe.model[PATCH_FLAG] = true;
    }

    install_sei_prospect_cache_bypass();
    document.addEventListener('DOMContentLoaded', install_sei_prospect_cache_bypass);
})();
