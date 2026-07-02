(() => {
  const APP_NAME = "sales_engagement_intelligence";

  function applyLogoUrl(item, icon) {
    if (!item || !icon || icon.app !== APP_NAME || !icon.logo_url) return;
    item.icon_url = icon.logo_url;
    delete item.icon;
    delete item.icon_html;
  }

  function patchSidebarHeader() {
    const SidebarHeader = frappe?.ui?.SidebarHeader;
    if (!SidebarHeader || SidebarHeader.__salesEngagementLogoUrlPatch) return;

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
      const iconByName = Object.fromEntries(
        (frappe.boot?.desktop_icons || [])
          .filter((icon) => icon.app === APP_NAME)
          .map((icon) => [icon.name, icon])
      );

      function applyToItem(item) {
        applyLogoUrl(item, iconByName[item.name]);
        (item.items || []).forEach(applyToItem);
      }

      items.forEach(applyToItem);
      return items;
    };

    SidebarHeader.__salesEngagementLogoUrlPatch = true;
  }

  frappe.after_ajax(patchSidebarHeader);
})();
