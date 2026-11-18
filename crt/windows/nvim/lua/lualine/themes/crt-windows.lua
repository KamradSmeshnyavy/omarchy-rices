-- Retro CRT Windows — lualine: NORMAL в сигнальном цвете, остальные режимы — роли палитры.
return {
  normal = { a = { fg = "#22272e", bg = "#909dab", gui = "bold" }, b = { fg = "#adbac7", bg = "#2d333a" }, c = { fg = "#8e9196", bg = "#292e36" } },
  insert = { a = { fg = "#22272e", bg = "#57ab5a", gui = "bold" }, b = { fg = "#adbac7", bg = "#2d333a" }, c = { fg = "#8e9196", bg = "#292e36" } },
  visual = { a = { fg = "#22272e", bg = "#909dab", gui = "bold" }, b = { fg = "#adbac7", bg = "#2d333a" }, c = { fg = "#8e9196", bg = "#292e36" } },
  replace = { a = { fg = "#22272e", bg = "#f47067", gui = "bold" }, b = { fg = "#adbac7", bg = "#2d333a" }, c = { fg = "#8e9196", bg = "#292e36" } },
  command = { a = { fg = "#22272e", bg = "#76e3ea", gui = "bold" }, b = { fg = "#adbac7", bg = "#2d333a" }, c = { fg = "#8e9196", bg = "#292e36" } },
  terminal = { a = { fg = "#22272e", bg = "#6cb6ff", gui = "bold" }, b = { fg = "#adbac7", bg = "#2d333a" }, c = { fg = "#8e9196", bg = "#292e36" } },
  inactive = { a = { fg = "#6e7378", bg = "#292e36" }, b = { fg = "#6e7378", bg = "#292e36" }, c = { fg = "#6e7378", bg = "#292e36" } },
}
