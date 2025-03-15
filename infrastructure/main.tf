resource "azurerm_storage_account" "fiscal_storage_account" {
  name                     = var.storage_account_name
  resource_group_name      = var.resource_group_name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  account_kind             = "StorageV2"
  is_hns_enabled           = "true"
}

resource "azurerm_storage_data_lake_gen2_filesystem" "fiscal_data_lake_filesystem" {
  name               = var.datalake_name
  storage_account_id = azurerm_storage_account.fiscal_storage_account.id
}