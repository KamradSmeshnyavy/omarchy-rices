-- Quest Dusk — lualine: NORMAL в сигнальном цвете, остальные режимы — роли палитры.
return {
  normal = { a = { fg = "#12081c", bg = "#ffb347", gui = "bold" }, b = { fg = "#f6eefa", bg = "#4a216a" }, c = { fg = "#d9bfeb", bg = "#391956" } },
  insert = { a = { fg = "#24103d", bg = "#7ee08a", gui = "bold" }, b = { fg = "#f6eefa", bg = "#4a216a" }, c = { fg = "#d9bfeb", bg = "#391956" } },
  visual = { a = { fg = "#24103d", bg = "#c598ac", gui = "bold" }, b = { fg = "#f6eefa", bg = "#4a216a" }, c = { fg = "#d9bfeb", bg = "#391956" } },
  replace = { a = { fg = "#24103d", bg = "#ff6a7a", gui = "bold" }, b = { fg = "#f6eefa", bg = "#4a216a" }, c = { fg = "#d9bfeb", bg = "#391956" } },
  command = { a = { fg = "#24103d", bg = "#7fd0e8", gui = "bold" }, b = { fg = "#f6eefa", bg = "#4a216a" }, c = { fg = "#d9bfeb", bg = "#391956" } },
  terminal = { a = { fg = "#24103d", bg = "#bca1cd", gui = "bold" }, b = { fg = "#f6eefa", bg = "#4a216a" }, c = { fg = "#d9bfeb", bg = "#391956" } },
  inactive = { a = { fg = "#9a82ae", bg = "#391956" }, b = { fg = "#9a82ae", bg = "#391956" }, c = { fg = "#9a82ae", bg = "#391956" } },
}
