-- Quest Classic: рамка окна — светлая рамка диалога, у неактивного — её внутренний цвет
-- (omarchy-themes/rices/quest/build.py). Толщину и углы задаёт стиль Customizer «quest».
hl.config({
	general = { col = { active_border = "rgb(f4f4f4)", inactive_border = "rgb(8f9ac8)" } },
	group = { col = { border_active = "rgb(f4f4f4)", border_inactive = "rgb(8f9ac8)" } },
})
