(() => {
  function applyLogoUrl(item, icon) {
    if (!item || !icon || !icon.logo_url) return;
    item.icon_url = icon.logo_url;
    delete item.icon;
    delete item.icon_html;
  }

  function patchSidebarHeader() {
    const SidebarHeader = frappe?.ui?.SidebarHeader;
    if (!SidebarHeader || SidebarHeader.__seiLogoUrlPatch) return;

    const originalGetIconForMenuItem = SidebarHeader.prototype.get_icon_for_menu_item;
    SidebarHeader.prototype.get_icon_for_menu_item = function (icon, item) {
      applyLogoUrl(item, icon);
      if (!item.icon_url && originalGetIconForMenuItem) {
        return originalGetIconForMenuItem.call(this, icon, item);
      }
    };

    const originalFetchRelatedIcons = SidebarHeader.prototype.fetch_related_icons;
    SidebarHeader.prototype.fetch_related_icons = function () {
      const items = originalFetchRelatedIcons.call(this) || [];
      const iconByLabel = Object.fromEntries(
        (frappe.boot?.desktop_icons || []).map((icon) => [icon.label, icon])
      );

      function applyToItem(item) {
        applyLogoUrl(item, iconByLabel[item.label]);
        (item.items || []).forEach(applyToItem);
      }

      items.forEach(applyToItem);
      return items;
    };

    SidebarHeader.__seiLogoUrlPatch = true;
  }

  frappe.after_ajax(patchSidebarHeader);
})();
