-- Quest Forest — lualine: NORMAL в сигнальном цвете, остальные режимы — роли палитры.
return {
  normal = { a = { fg = "#06140c", bg = "#f5e663", gui = "bold" }, b = { fg = "#f2f8ee", bg = "#1d5738" }, c = { fg = "#bde4c4", bg = "#15442c" } },
  insert = { a = { fg = "#0b2d1d", bg = "#8ee06a", gui = "bold" }, b = { fg = "#f2f8ee", bg = "#1d5738" }, c = { fg = "#bde4c4", bg = "#15442c" } },
  visual = { a = { fg = "#0b2d1d", bg = "#bea296", gui = "bold" }, b = { fg = "#f2f8ee", bg = "#1d5738" }, c = { fg = "#bde4c4", bg = "#15442c" } },
  replace = { a = { fg = "#0b2d1d", bg = "#ff7a5a", gui = "bold" }, b = { fg = "#f2f8ee", bg = "#1d5738" }, c = { fg = "#bde4c4", bg = "#15442c" } },
  command = { a = { fg = "#0b2d1d", bg = "#6fd3e0", gui = "bold" }, b = { fg = "#f2f8ee", bg = "#1d5738" }, c = { fg = "#bde4c4", bg = "#15442c" } },
  terminal = { a = { fg = "#0b2d1d", bg = "#a0c3af", gui = "bold" }, b = { fg = "#f2f8ee", bg = "#1d5738" }, c = { fg = "#bde4c4", bg = "#15442c" } },
  inactive = { a = { fg = "#7fa48a", bg = "#15442c" }, b = { fg = "#7fa48a", bg = "#15442c" }, c = { fg = "#7fa48a", bg = "#15442c" } },
}
