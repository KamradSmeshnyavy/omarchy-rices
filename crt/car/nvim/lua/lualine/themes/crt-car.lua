-- Retro CRT Car — lualine: NORMAL в сигнальном цвете, остальные режимы — роли палитры.
return {
  normal = { a = { fg = "#282828", bg = "#8ec07c", gui = "bold" }, b = { fg = "#ebdbb2", bg = "#323730" }, c = { fg = "#9f9184", bg = "#2e312d" } },
  insert = { a = { fg = "#282828", bg = "#b8bb26", gui = "bold" }, b = { fg = "#ebdbb2", bg = "#323730" }, c = { fg = "#9f9184", bg = "#2e312d" } },
  visual = { a = { fg = "#282828", bg = "#8ec07c", gui = "bold" }, b = { fg = "#ebdbb2", bg = "#323730" }, c = { fg = "#9f9184", bg = "#2e312d" } },
  replace = { a = { fg = "#282828", bg = "#fb5440", gui = "bold" }, b = { fg = "#ebdbb2", bg = "#323730" }, c = { fg = "#9f9184", bg = "#2e312d" } },
  command = { a = { fg = "#282828", bg = "#8ec07c", gui = "bold" }, b = { fg = "#ebdbb2", bg = "#323730" }, c = { fg = "#9f9184", bg = "#2e312d" } },
  terminal = { a = { fg = "#282828", bg = "#83a598", gui = "bold" }, b = { fg = "#ebdbb2", bg = "#323730" }, c = { fg = "#9f9184", bg = "#2e312d" } },
  inactive = { a = { fg = "#928374", bg = "#2e312d" }, b = { fg = "#928374", bg = "#2e312d" }, c = { fg = "#928374", bg = "#2e312d" } },
}
