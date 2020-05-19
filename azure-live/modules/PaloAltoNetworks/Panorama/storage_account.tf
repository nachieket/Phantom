# Storage account for boot diagnostics

resource "random_id" "storage_account" {
  byte_length = 4
}

resource "azurerm_storage_account" "mystorageaccount" {
  name                     = "${var.diagnosticsStorageAccountName}${lower(random_id.storage_account.hex)}"
  location                 = var.resourcegroup_location
  resource_group_name      = var.resourcegroup_name
  account_tier             = var.diagnosticsStorageAccountTier
  account_replication_type = var.diagnosticsStorageAccountReplication
}
