
import matplotlib.cm as cm
import numpy as np
import matplotlib.tri as mtri


# import matplotlib.pyplot as plt
# 绘制热液系统MATLAB程序导出的温度场等
def plot_VAR(X, Y, triangles, var, plot, ax, n_level_surf=50, vmin='', vmax='', cmp0='rainbow',
             cmap_under='k', cmap_over='w', num_tick_cb=5,
             contour=True, levels_c=[], color_contour='k', linewidth_contour=1, clabels=[], fmt_cb='%.0f', label_cb=''):
    #     contourf\
    extend = 'neither'
    cmap_surf = cm.get_cmap(name=cmp0, lut=None)
    if(vmin == ''):
        vmin = var.min()
    else:
        cmap_surf.set_under(cmap_under)
        extend = 'min'
    if(vmax == ''):
        vmax = var.max()
    else:
        cmap_surf.set_over(cmap_over)
        if(extend == 'min'):
            extend = 'both'
        else:
            extend = 'max'
    levels_surf = np.linspace(vmin, vmax, n_level_surf)

    CS = ax.tricontourf(X, Y, triangles, var,
                        levels=levels_surf, cmap=cmap_surf, extend=extend)
    for a in CS.collections:
        a.set_edgecolor('face')
        a.set_linewidth(0.001)
    #         contour
    colors = []
    linewidths = []
    for i in range(0, len(levels_c)):
        colors.append(color_contour)
        linewidths.append(linewidth_contour)
    if(len(levels_c) > 0):
        Contour = ax.tricontour(
            X, Y, triangles, var, levels=levels_c, colors=colors, linewidths=linewidths)
        if(len(clabels) > 0):
            ax.clabel(Contour, Contour.levels, inline=True, fontsize=5)
    #     colorbar
    ticks = np.linspace(vmin, vmax, num_tick_cb)
    d_ticks = ticks[1]-ticks[0]
    ind_del = ticks > vmax
    for i in range(0, len(levels_c)):  # find which values near the levels_c
        dif = np.abs(ticks-levels_c[i])
        ind_del = ind_del | (dif < d_ticks/3)
    ind_del = np.where(ind_del == True)
    ticks = np.delete(ticks, ind_del)   # delete the near values
    ticks = np.append(ticks, levels_c)
    ticks = np.sort(ticks)
    #     location
    cb = plot.colorbar(CS, format=fmt_cb,
                       orientation='vertical', pad=0.01, ticks=ticks)
    if(len(levels_c) > 0):
        cb.add_lines(Contour)
    cb.set_label(label_cb)
    cb.solids.set_edgecolor("face")

    #     set colorbar near figure
    ax.set_aspect('auto')
