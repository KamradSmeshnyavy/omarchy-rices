-- Quest Dungeon — lualine: NORMAL в сигнальном цвете, остальные режимы — роли палитры.
return {
  normal = { a = { fg = "#050102", bg = "#ff3b30", gui = "bold" }, b = { fg = "#ece0c8", bg = "#28090d" }, c = { fg = "#b39a80", bg = "#1e070a" } },
  insert = { a = { fg = "#120406", bg = "#e0453a", gui = "bold" }, b = { fg = "#ece0c8", bg = "#28090d" }, c = { fg = "#b39a80", bg = "#1e070a" } },
  visual = { a = { fg = "#120406", bg = "#c86a9a", gui = "bold" }, b = { fg = "#ece0c8", bg = "#28090d" }, c = { fg = "#b39a80", bg = "#1e070a" } },
  replace = { a = { fg = "#050102", bg = "#ff3b30", gui = "bold" }, b = { fg = "#ece0c8", bg = "#28090d" }, c = { fg = "#b39a80", bg = "#1e070a" } },
  command = { a = { fg = "#120406", bg = "#9a7ae8", gui = "bold" }, b = { fg = "#ece0c8", bg = "#28090d" }, c = { fg = "#b39a80", bg = "#1e070a" } },
  terminal = { a = { fg = "#120406", bg = "#a69294", gui = "bold" }, b = { fg = "#ece0c8", bg = "#28090d" }, c = { fg = "#b39a80", bg = "#1e070a" } },
  inactive = { a = { fg = "#7b6655", bg = "#1e070a" }, b = { fg = "#7b6655", bg = "#1e070a" }, c = { fg = "#7b6655", bg = "#1e070a" } },
}
