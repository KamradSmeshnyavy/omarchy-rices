-- Space Atlas — lualine: NORMAL в сигнальном цвете, остальные режимы — роли палитры.
return {
  normal = { a = { fg = "#2e3440", bg = "#bf616a", gui = "bold" }, b = { fg = "#d8dee9", bg = "#3f4551" }, c = { fg = "#989ea9", bg = "#363c48" } },
  insert = { a = { fg = "#2e3440", bg = "#a3be8c", gui = "bold" }, b = { fg = "#d8dee9", bg = "#3f4551" }, c = { fg = "#989ea9", bg = "#363c48" } },
  visual = { a = { fg = "#2e3440", bg = "#d08a91", gui = "bold" }, b = { fg = "#d8dee9", bg = "#3f4551" }, c = { fg = "#989ea9", bg = "#363c48" } },
  replace = { a = { fg = "#2e3440", bg = "#d08a91", gui = "bold" }, b = { fg = "#d8dee9", bg = "#3f4551" }, c = { fg = "#989ea9", bg = "#363c48" } },
  command = { a = { fg = "#2e3440", bg = "#88c0d0", gui = "bold" }, b = { fg = "#d8dee9", bg = "#3f4551" }, c = { fg = "#989ea9", bg = "#363c48" } },
  terminal = { a = { fg = "#2e3440", bg = "#81a1c1", gui = "bold" }, b = { fg = "#d8dee9", bg = "#3f4551" }, c = { fg = "#989ea9", bg = "#363c48" } },
  inactive = { a = { fg = "#7b8391", bg = "#363c48" }, b = { fg = "#7b8391", bg = "#363c48" }, c = { fg = "#7b8391", bg = "#363c48" } },
}
