(() => {
    const PATCH_FLAG = '__sei_prospect_doctype_cache_bypass';

    function install_sei_prospect_doctype_cache_bypass() {
        if (!window.frappe?.model?.with_doctype || frappe.model[PATCH_FLAG]) return;

        const original_with_doctype = frappe.model.with_doctype.bind(frappe.model);
        let prospect_meta_refreshed = false;

        frappe.model.with_doctype = function (doctype, callback, async) {
            if (doctype === 'SEI Prospect' && !prospect_meta_refreshed) {
                prospect_meta_refreshed = true;
                if (window.locals?.DocType?.[doctype]) {
                    delete window.locals.DocType[doctype];
                }
            }
            return original_with_doctype(doctype, callback, async);
        };

        frappe.model[PATCH_FLAG] = true;
    }

    install_sei_prospect_doctype_cache_bypass();
    document.addEventListener('DOMContentLoaded', install_sei_prospect_doctype_cache_bypass);
})();
