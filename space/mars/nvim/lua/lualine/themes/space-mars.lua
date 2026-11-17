-- Space Mars — lualine: NORMAL в сигнальном цвете, остальные режимы — роли палитры.
return {
  normal = { a = { fg = "#282828", bg = "#fb4934", gui = "bold" }, b = { fg = "#ebdbb2", bg = "#3c3a36" }, c = { fg = "#968f8a", bg = "#32312f" } },
  insert = { a = { fg = "#282828", bg = "#b8bb26", gui = "bold" }, b = { fg = "#ebdbb2", bg = "#3c3a36" }, c = { fg = "#968f8a", bg = "#32312f" } },
  visual = { a = { fg = "#282828", bg = "#fb5440", gui = "bold" }, b = { fg = "#ebdbb2", bg = "#3c3a36" }, c = { fg = "#968f8a", bg = "#32312f" } },
  replace = { a = { fg = "#282828", bg = "#fb5440", gui = "bold" }, b = { fg = "#ebdbb2", bg = "#3c3a36" }, c = { fg = "#968f8a", bg = "#32312f" } },
  command = { a = { fg = "#282828", bg = "#8ec07c", gui = "bold" }, b = { fg = "#ebdbb2", bg = "#3c3a36" }, c = { fg = "#968f8a", bg = "#32312f" } },
  terminal = { a = { fg = "#282828", bg = "#83a598", gui = "bold" }, b = { fg = "#ebdbb2", bg = "#3c3a36" }, c = { fg = "#968f8a", bg = "#32312f" } },
  inactive = { a = { fg = "#807871", bg = "#32312f" }, b = { fg = "#807871", bg = "#32312f" }, c = { fg = "#807871", bg = "#32312f" } },
}
