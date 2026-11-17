-- Space Dusk — lualine: NORMAL в сигнальном цвете, остальные режимы — роли палитры.
return {
  normal = { a = { fg = "#282a36", bg = "#ff79c6", gui = "bold" }, b = { fg = "#f8f8f2", bg = "#3d3f49" }, c = { fg = "#8491b8", bg = "#32343f" } },
  insert = { a = { fg = "#282a36", bg = "#50fa7b", gui = "bold" }, b = { fg = "#f8f8f2", bg = "#3d3f49" }, c = { fg = "#8491b8", bg = "#32343f" } },
  visual = { a = { fg = "#282a36", bg = "#ff79c6", gui = "bold" }, b = { fg = "#f8f8f2", bg = "#3d3f49" }, c = { fg = "#8491b8", bg = "#32343f" } },
  replace = { a = { fg = "#282a36", bg = "#ff5555", gui = "bold" }, b = { fg = "#f8f8f2", bg = "#3d3f49" }, c = { fg = "#8491b8", bg = "#32343f" } },
  command = { a = { fg = "#282a36", bg = "#ff79c6", gui = "bold" }, b = { fg = "#f8f8f2", bg = "#3d3f49" }, c = { fg = "#8491b8", bg = "#32343f" } },
  terminal = { a = { fg = "#282a36", bg = "#8be9fd", gui = "bold" }, b = { fg = "#f8f8f2", bg = "#3d3f49" }, c = { fg = "#8491b8", bg = "#32343f" } },
  inactive = { a = { fg = "#6272a4", bg = "#32343f" }, b = { fg = "#6272a4", bg = "#32343f" }, c = { fg = "#6272a4", bg = "#32343f" } },
}
