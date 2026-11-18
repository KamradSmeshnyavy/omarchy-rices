-- Retro CRT Phosphor — lualine: NORMAL в сигнальном цвете, остальные режимы — роли палитры.
return {
  normal = { a = { fg = "#000000", bg = "#1aff53", gui = "bold" }, b = { fg = "#5ae27c", bg = "#031a08" }, c = { fg = "#60846a", bg = "#020f05" } },
  insert = { a = { fg = "#000000", bg = "#00c230", gui = "bold" }, b = { fg = "#5ae27c", bg = "#031a08" }, c = { fg = "#60846a", bg = "#020f05" } },
  visual = { a = { fg = "#000000", bg = "#1aff53", gui = "bold" }, b = { fg = "#5ae27c", bg = "#031a08" }, c = { fg = "#60846a", bg = "#020f05" } },
  replace = { a = { fg = "#000000", bg = "#14cb0b", gui = "bold" }, b = { fg = "#5ae27c", bg = "#031a08" }, c = { fg = "#60846a", bg = "#020f05" } },
  command = { a = { fg = "#000000", bg = "#16ca79", gui = "bold" }, b = { fg = "#5ae27c", bg = "#031a08" }, c = { fg = "#60846a", bg = "#020f05" } },
  terminal = { a = { fg = "#000000", bg = "#19e696", gui = "bold" }, b = { fg = "#5ae27c", bg = "#031a08" }, c = { fg = "#60846a", bg = "#020f05" } },
  inactive = { a = { fg = "#406b4b", bg = "#020f05" }, b = { fg = "#406b4b", bg = "#020f05" }, c = { fg = "#406b4b", bg = "#020f05" } },
}
