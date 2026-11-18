-- Retro CRT Amber — lualine: NORMAL в сигнальном цвете, остальные режимы — роли палитры.
return {
  normal = { a = { fg = "#000000", bg = "#ffaa1a", gui = "bold" }, b = { fg = "#e2b05a", bg = "#1a1103" }, c = { fg = "#847760", bg = "#0f0a02" } },
  insert = { a = { fg = "#000000", bg = "#c27a00", gui = "bold" }, b = { fg = "#e2b05a", bg = "#1a1103" }, c = { fg = "#847760", bg = "#0f0a02" } },
  visual = { a = { fg = "#000000", bg = "#ffaa1a", gui = "bold" }, b = { fg = "#e2b05a", bg = "#1a1103" }, c = { fg = "#847760", bg = "#0f0a02" } },
  replace = { a = { fg = "#000000", bg = "#cb4a0b", gui = "bold" }, b = { fg = "#e2b05a", bg = "#1a1103" }, c = { fg = "#847760", bg = "#0f0a02" } },
  command = { a = { fg = "#000000", bg = "#cabd16", gui = "bold" }, b = { fg = "#e2b05a", bg = "#1a1103" }, c = { fg = "#847760", bg = "#0f0a02" } },
  terminal = { a = { fg = "#000000", bg = "#e6e319", gui = "bold" }, b = { fg = "#e2b05a", bg = "#1a1103" }, c = { fg = "#847760", bg = "#0f0a02" } },
  inactive = { a = { fg = "#6b5b40", bg = "#0f0a02" }, b = { fg = "#6b5b40", bg = "#0f0a02" }, c = { fg = "#6b5b40", bg = "#0f0a02" } },
}
