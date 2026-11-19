-- Modern Zen — lualine: NORMAL в сигнальном цвете, остальные режимы — роли палитры.
return {
  normal = { a = { fg = "#1e1f25", bg = "#817e63", gui = "bold" }, b = { fg = "#95989f", bg = "#2b2c32" }, c = { fg = "#8a8b91", bg = "#25262c" } },
  insert = { a = { fg = "#1e1f25", bg = "#818b74", gui = "bold" }, b = { fg = "#95989f", bg = "#2b2c32" }, c = { fg = "#8a8b91", bg = "#25262c" } },
  visual = { a = { fg = "#1e1f25", bg = "#908d75", gui = "bold" }, b = { fg = "#95989f", bg = "#2b2c32" }, c = { fg = "#8a8b91", bg = "#25262c" } },
  replace = { a = { fg = "#1e1f25", bg = "#8a8a7a", gui = "bold" }, b = { fg = "#95989f", bg = "#2b2c32" }, c = { fg = "#8a8b91", bg = "#25262c" } },
  command = { a = { fg = "#1e1f25", bg = "#b4b289", gui = "bold" }, b = { fg = "#95989f", bg = "#2b2c32" }, c = { fg = "#8a8b91", bg = "#25262c" } },
  terminal = { a = { fg = "#1e1f25", bg = "#a09d76", gui = "bold" }, b = { fg = "#95989f", bg = "#2b2c32" }, c = { fg = "#8a8b91", bg = "#25262c" } },
  inactive = { a = { fg = "#6c7081", bg = "#25262c" }, b = { fg = "#6c7081", bg = "#25262c" }, c = { fg = "#6c7081", bg = "#25262c" } },
}
