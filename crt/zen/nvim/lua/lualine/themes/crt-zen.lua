-- Retro CRT Zen — lualine: NORMAL в сигнальном цвете, остальные режимы — роли палитры.
return {
  normal = { a = { fg = "#0e1a20", bg = "#6f675f", gui = "bold" }, b = { fg = "#c2c5c7", bg = "#182226" }, c = { fg = "#79848a", bg = "#141f24" } },
  insert = { a = { fg = "#0e1a20", bg = "#9d7d75", gui = "bold" }, b = { fg = "#c2c5c7", bg = "#182226" }, c = { fg = "#79848a", bg = "#141f24" } },
  visual = { a = { fg = "#0e1a20", bg = "#88817a", gui = "bold" }, b = { fg = "#c2c5c7", bg = "#182226" }, c = { fg = "#79848a", bg = "#141f24" } },
  replace = { a = { fg = "#0e1a20", bg = "#898480", gui = "bold" }, b = { fg = "#c2c5c7", bg = "#182226" }, c = { fg = "#79848a", bg = "#141f24" } },
  command = { a = { fg = "#0e1a20", bg = "#a57b6a", gui = "bold" }, b = { fg = "#c2c5c7", bg = "#182226" }, c = { fg = "#79848a", bg = "#141f24" } },
  terminal = { a = { fg = "#0e1a20", bg = "#858887", gui = "bold" }, b = { fg = "#c2c5c7", bg = "#182226" }, c = { fg = "#79848a", bg = "#141f24" } },
  inactive = { a = { fg = "#5d6b72", bg = "#141f24" }, b = { fg = "#5d6b72", bg = "#141f24" }, c = { fg = "#5d6b72", bg = "#141f24" } },
}
