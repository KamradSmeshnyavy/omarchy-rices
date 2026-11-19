-- Modern Default — lualine: NORMAL в сигнальном цвете, остальные режимы — роли палитры.
return {
  normal = { a = { fg = "#0f2024", bg = "#b26e4e", gui = "bold" }, b = { fg = "#929a9c", bg = "#1d2d31" }, c = { fg = "#838c8f", bg = "#17272b" } },
  insert = { a = { fg = "#0f2024", bg = "#479189", gui = "bold" }, b = { fg = "#929a9c", bg = "#1d2d31" }, c = { fg = "#838c8f", bg = "#17272b" } },
  visual = { a = { fg = "#0f2024", bg = "#b77759", gui = "bold" }, b = { fg = "#929a9c", bg = "#1d2d31" }, c = { fg = "#838c8f", bg = "#17272b" } },
  replace = { a = { fg = "#0f2024", bg = "#a5806e", gui = "bold" }, b = { fg = "#929a9c", bg = "#1d2d31" }, c = { fg = "#838c8f", bg = "#17272b" } },
  command = { a = { fg = "#0f2024", bg = "#e5965f", gui = "bold" }, b = { fg = "#929a9c", bg = "#1d2d31" }, c = { fg = "#838c8f", bg = "#17272b" } },
  terminal = { a = { fg = "#0f2024", bg = "#aa9473", gui = "bold" }, b = { fg = "#929a9c", bg = "#1d2d31" }, c = { fg = "#838c8f", bg = "#17272b" } },
  inactive = { a = { fg = "#5e7074", bg = "#17272b" }, b = { fg = "#5e7074", bg = "#17272b" }, c = { fg = "#5e7074", bg = "#17272b" } },
}
