module "azurerm_storage_account" {
  source              = "github.com/sc-azure"
  storage_accounts    = var.storage_accounts
}