-- Space Frost — lualine: NORMAL в сигнальном цвете, остальные режимы — роли палитры.
return {
  normal = { a = { fg = "#24283b", bg = "#7dcfff", gui = "bold" }, b = { fg = "#c0caf5", bg = "#34384e" }, c = { fg = "#8a91ae", bg = "#2c3044" } },
  insert = { a = { fg = "#24283b", bg = "#9ece6a", gui = "bold" }, b = { fg = "#c0caf5", bg = "#34384e" }, c = { fg = "#8a91ae", bg = "#2c3044" } },
  visual = { a = { fg = "#24283b", bg = "#7dcfff", gui = "bold" }, b = { fg = "#c0caf5", bg = "#34384e" }, c = { fg = "#8a91ae", bg = "#2c3044" } },
  replace = { a = { fg = "#24283b", bg = "#f7768e", gui = "bold" }, b = { fg = "#c0caf5", bg = "#34384e" }, c = { fg = "#8a91ae", bg = "#2c3044" } },
  command = { a = { fg = "#24283b", bg = "#7dcfff", gui = "bold" }, b = { fg = "#c0caf5", bg = "#34384e" }, c = { fg = "#8a91ae", bg = "#2c3044" } },
  terminal = { a = { fg = "#24283b", bg = "#7aa2f7", gui = "bold" }, b = { fg = "#c0caf5", bg = "#34384e" }, c = { fg = "#8a91ae", bg = "#2c3044" } },
  inactive = { a = { fg = "#6a7297", bg = "#2c3044" }, b = { fg = "#6a7297", bg = "#2c3044" }, c = { fg = "#6a7297", bg = "#2c3044" } },
}
