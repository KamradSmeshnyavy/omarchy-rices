-- Retro CRT Arcade — lualine: NORMAL в сигнальном цвете, остальные режимы — роли палитры.
return {
  normal = { a = { fg = "#0c0e1d", bg = "#525669", gui = "bold" }, b = { fg = "#c2c2c6", bg = "#131525" }, c = { fg = "#787a89", bg = "#101222" } },
  insert = { a = { fg = "#0c0e1d", bg = "#797b86", gui = "bold" }, b = { fg = "#c2c2c6", bg = "#131525" }, c = { fg = "#787a89", bg = "#101222" } },
  visual = { a = { fg = "#0c0e1d", bg = "#787b8a", gui = "bold" }, b = { fg = "#c2c2c6", bg = "#131525" }, c = { fg = "#787a89", bg = "#101222" } },
  replace = { a = { fg = "#0c0e1d", bg = "#7a7b85", gui = "bold" }, b = { fg = "#c2c2c6", bg = "#131525" }, c = { fg = "#787a89", bg = "#101222" } },
  command = { a = { fg = "#0c0e1d", bg = "#768092", gui = "bold" }, b = { fg = "#c2c2c6", bg = "#131525" }, c = { fg = "#787a89", bg = "#101222" } },
  terminal = { a = { fg = "#0c0e1d", bg = "#857a84", gui = "bold" }, b = { fg = "#c2c2c6", bg = "#131525" }, c = { fg = "#787a89", bg = "#101222" } },
  inactive = { a = { fg = "#5c5e70", bg = "#101222" }, b = { fg = "#5c5e70", bg = "#101222" }, c = { fg = "#5c5e70", bg = "#101222" } },
}
