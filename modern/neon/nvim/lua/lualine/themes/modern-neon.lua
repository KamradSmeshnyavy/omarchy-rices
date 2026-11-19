-- Modern Neon — lualine: NORMAL в сигнальном цвете, остальные режимы — роли палитры.
return {
  normal = { a = { fg = "#0e1721", bg = "#314c6c", gui = "bold" }, b = { fg = "#91959b", bg = "#1c252e" }, c = { fg = "#7b8086", bg = "#161f28" } },
  insert = { a = { fg = "#0e1721", bg = "#8584a0", gui = "bold" }, b = { fg = "#91959b", bg = "#1c252e" }, c = { fg = "#7b8086", bg = "#161f28" } },
  visual = { a = { fg = "#0e1721", bg = "#718399", gui = "bold" }, b = { fg = "#91959b", bg = "#1c252e" }, c = { fg = "#7b8086", bg = "#161f28" } },
  replace = { a = { fg = "#0e1721", bg = "#7a8695", gui = "bold" }, b = { fg = "#91959b", bg = "#1c252e" }, c = { fg = "#7b8086", bg = "#161f28" } },
  command = { a = { fg = "#0e1721", bg = "#a073b1", gui = "bold" }, b = { fg = "#91959b", bg = "#1c252e" }, c = { fg = "#7b8086", bg = "#161f28" } },
  terminal = { a = { fg = "#0e1721", bg = "#8081a9", gui = "bold" }, b = { fg = "#91959b", bg = "#1c252e" }, c = { fg = "#7b8086", bg = "#161f28" } },
  inactive = { a = { fg = "#5d6772", bg = "#161f28" }, b = { fg = "#5d6772", bg = "#161f28" }, c = { fg = "#5d6772", bg = "#161f28" } },
}
