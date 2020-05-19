provider "azurerm" {
  version = "=2.7.0"

  subscription_id = var.subscription_id
  tenant_id       = var.tenant_id
  client_id       = var.client_id
  client_secret   = var.client_secret

  features {
    virtual_machine {
      delete_os_disk_on_deletion = true
    }
  }
}

#### CREATE Panorama

resource "azurerm_virtual_machine" "panorama" {
  name                  = var.virtualMachineName
  location              = var.resourcegroup_location
  resource_group_name   = var.resourcegroup_name
  network_interface_ids = [azurerm_network_interface.panorama.id]

  primary_network_interface_id = azurerm_network_interface.panorama.id
  vm_size                      = var.virtualMachineSize # Change the Size

  plan {
    name      = "byol"
    publisher = "paloaltonetworks"
    product   = "panorama"
  }

  storage_image_reference {
    publisher = "paloaltonetworks"
    offer     = "panorama"
    sku       = "byol"
    version   = var.panoramaVersion
  }

  storage_os_disk {
    name              = var.virtualMachineName
    caching           = "ReadWrite"
    create_option     = "FromImage"
    managed_disk_type = "StandardSSD_LRS"
  }

  delete_os_disk_on_termination    = true
  delete_data_disks_on_termination = true

  os_profile {
    computer_name  = var.virtualMachineName
    admin_username = var.adminUsername
    admin_password = var.adminPassword
  }

  os_profile_linux_config {
    disable_password_authentication = false
  }

  boot_diagnostics {
    enabled     = "true"
    storage_uri = azurerm_storage_account.mystorageaccount.primary_blob_endpoint
  }
}
