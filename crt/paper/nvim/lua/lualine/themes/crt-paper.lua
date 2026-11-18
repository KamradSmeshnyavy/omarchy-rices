-- Retro CRT Paper — lualine: NORMAL в сигнальном цвете, остальные режимы — роли палитры.
return {
  normal = { a = { fg = "#000000", bg = "#f0eee0", gui = "bold" }, b = { fg = "#c9c7b8", bg = "#181816" }, c = { fg = "#7a7a73", bg = "#0e0e0d" } },
  insert = { a = { fg = "#000000", bg = "#7e7d69", gui = "bold" }, b = { fg = "#c9c7b8", bg = "#181816" }, c = { fg = "#7a7a73", bg = "#0e0e0d" } },
  visual = { a = { fg = "#000000", bg = "#f0eee0", gui = "bold" }, b = { fg = "#c9c7b8", bg = "#181816" }, c = { fg = "#7a7a73", bg = "#0e0e0d" } },
  replace = { a = { fg = "#000000", bg = "#7f786a", gui = "bold" }, b = { fg = "#c9c7b8", bg = "#181816" }, c = { fg = "#7a7a73", bg = "#0e0e0d" } },
  command = { a = { fg = "#000000", bg = "#757b65", gui = "bold" }, b = { fg = "#c9c7b8", bg = "#181816" }, c = { fg = "#7a7a73", bg = "#0e0e0d" } },
  terminal = { a = { fg = "#000000", bg = "#848c73", gui = "bold" }, b = { fg = "#c9c7b8", bg = "#181816" }, c = { fg = "#7a7a73", bg = "#0e0e0d" } },
  inactive = { a = { fg = "#5f5e56", bg = "#0e0e0d" }, b = { fg = "#5f5e56", bg = "#0e0e0d" }, c = { fg = "#5f5e56", bg = "#0e0e0d" } },
}
