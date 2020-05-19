#### CREATE PUBLIC IP ADDRESSES ####

resource "azurerm_public_ip" panorama {
  name                = var.publicIpAddressName
  location            = var.resourcegroup_location
  resource_group_name = var.resourcegroup_name
  allocation_method   = "Static"
}
