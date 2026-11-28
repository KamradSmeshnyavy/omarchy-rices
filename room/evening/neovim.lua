-- Своя colorscheme room-evening: лежит в каталоге темы (nvim/colors, nvim/lua/lualine/themes),
-- omarchy копирует тему в ~/.local/state/omarchy/current/theme — оттуда её и грузим.
return {
	{
		dir = vim.fn.expand("~/.local/state/omarchy/current/theme/nvim"),
		name = "room-evening",
		lazy = false,
		priority = 1000,
	},
	{
		"LazyVim/LazyVim",
		opts = {
			colorscheme = "room-evening",
		},
	},
}
