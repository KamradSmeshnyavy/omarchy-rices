-- Quest Parchment — lualine: NORMAL в сигнальном цвете, остальные режимы — роли палитры.
return {
  normal = { a = { fg = "#f8efd6", bg = "#b0302a", gui = "bold" }, b = { fg = "#2e2216", bg = "#f0e4c1" }, c = { fg = "#6e5636", bg = "#f4e9cb" } },
  insert = { a = { fg = "#f8efd6", bg = "#3d7a2a", gui = "bold" }, b = { fg = "#2e2216", bg = "#f0e4c1" }, c = { fg = "#6e5636", bg = "#f4e9cb" } },
  visual = { a = { fg = "#f8efd6", bg = "#74435c", gui = "bold" }, b = { fg = "#2e2216", bg = "#f0e4c1" }, c = { fg = "#6e5636", bg = "#f4e9cb" } },
  replace = { a = { fg = "#f8efd6", bg = "#b0302a", gui = "bold" }, b = { fg = "#2e2216", bg = "#f0e4c1" }, c = { fg = "#6e5636", bg = "#f4e9cb" } },
  command = { a = { fg = "#f8efd6", bg = "#2a5a9a", gui = "bold" }, b = { fg = "#2e2216", bg = "#f0e4c1" }, c = { fg = "#6e5636", bg = "#f4e9cb" } },
  terminal = { a = { fg = "#f8efd6", bg = "#706c60", gui = "bold" }, b = { fg = "#2e2216", bg = "#f0e4c1" }, c = { fg = "#6e5636", bg = "#f4e9cb" } },
  inactive = { a = { fg = "#968568", bg = "#f4e9cb" }, b = { fg = "#968568", bg = "#f4e9cb" }, c = { fg = "#968568", bg = "#f4e9cb" } },
}
