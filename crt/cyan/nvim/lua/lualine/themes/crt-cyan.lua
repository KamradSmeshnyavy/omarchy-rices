-- Retro CRT Cyan — lualine: NORMAL в сигнальном цвете, остальные режимы — роли палитры.
return {
  normal = { a = { fg = "#000000", bg = "#1affff", gui = "bold" }, b = { fg = "#5ae2e2", bg = "#031a1a" }, c = { fg = "#567c7c", bg = "#020f0f" } },
  insert = { a = { fg = "#000000", bg = "#00c2c2", gui = "bold" }, b = { fg = "#5ae2e2", bg = "#031a1a" }, c = { fg = "#567c7c", bg = "#020f0f" } },
  visual = { a = { fg = "#000000", bg = "#1affff", gui = "bold" }, b = { fg = "#5ae2e2", bg = "#031a1a" }, c = { fg = "#567c7c", bg = "#020f0f" } },
  replace = { a = { fg = "#000000", bg = "#0bcb92", gui = "bold" }, b = { fg = "#5ae2e2", bg = "#031a1a" }, c = { fg = "#567c7c", bg = "#020f0f" } },
  command = { a = { fg = "#000000", bg = "#1694ca", gui = "bold" }, b = { fg = "#5ae2e2", bg = "#031a1a" }, c = { fg = "#567c7c", bg = "#020f0f" } },
  terminal = { a = { fg = "#000000", bg = "#199ce6", gui = "bold" }, b = { fg = "#5ae2e2", bg = "#031a1a" }, c = { fg = "#567c7c", bg = "#020f0f" } },
  inactive = { a = { fg = "#346262", bg = "#020f0f" }, b = { fg = "#346262", bg = "#020f0f" }, c = { fg = "#346262", bg = "#020f0f" } },
}
