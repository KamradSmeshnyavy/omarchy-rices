-- Quest Classic — lualine: NORMAL в сигнальном цвете, остальные режимы — роли палитры.
return {
  normal = { a = { fg = "#0a0c20", bg = "#ffd84a", gui = "bold" }, b = { fg = "#f4f4f4", bg = "#1d3698" }, c = { fg = "#a9b4e8", bg = "#162981" } },
  insert = { a = { fg = "#0d1a66", bg = "#5ee06a", gui = "bold" }, b = { fg = "#f4f4f4", bg = "#1d3698" }, c = { fg = "#a9b4e8", bg = "#162981" } },
  visual = { a = { fg = "#0d1a66", bg = "#b68ba4", gui = "bold" }, b = { fg = "#f4f4f4", bg = "#1d3698" }, c = { fg = "#a9b4e8", bg = "#162981" } },
  replace = { a = { fg = "#0d1a66", bg = "#ff6a5a", gui = "bold" }, b = { fg = "#f4f4f4", bg = "#1d3698" }, c = { fg = "#a9b4e8", bg = "#162981" } },
  command = { a = { fg = "#0d1a66", bg = "#5cb4ff", gui = "bold" }, b = { fg = "#f4f4f4", bg = "#1d3698" }, c = { fg = "#a9b4e8", bg = "#162981" } },
  terminal = { a = { fg = "#0d1a66", bg = "#9faee3", gui = "bold" }, b = { fg = "#f4f4f4", bg = "#1d3698" }, c = { fg = "#a9b4e8", bg = "#162981" } },
  inactive = { a = { fg = "#727eba", bg = "#162981" }, b = { fg = "#727eba", bg = "#162981" }, c = { fg = "#727eba", bg = "#162981" } },
}
