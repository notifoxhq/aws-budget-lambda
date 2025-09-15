variable "NOTIFOX_AUDIENCE" {
  type        = string
  description = "The audience to send the alert to"
}

variable "NOTIFOX_API_KEY" {
  type        = string
  description = "Your notifox API token"
  sensitive   = true
}