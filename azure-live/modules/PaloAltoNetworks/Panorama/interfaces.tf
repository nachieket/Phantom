#### CREATE THE NETWORK INTERFACES ####

resource "azurerm_network_interface" "panorama" {
  name                = var.networkInterfaceName
  location            = var.resourcegroup_location
  resource_group_name = var.resourcegroup_name

  ip_configuration {
    name                          = var.networkInterfaceName
    subnet_id                     = var.azure_subnet_id
    private_ip_address_allocation = "Static"
    private_ip_address            = var.panorama_ip_address
    public_ip_address_id          = azurerm_public_ip.panorama.id
  }

  depends_on = ["azurerm_public_ip.panorama"]
}