
import matplotlib.cm as cm
import numpy as np
import matplotlib.tri as mtri


import numpy as np


def plot_boundary(X, Y, PointID, BoundaryPolygon_ptID, ax, colors=['r', 'm', 'k']):
    for i in range(0, len(BoundaryPolygon_ptID)):
        if (i == (len(BoundaryPolygon_ptID) - 1)):
            x = [X[BoundaryPolygon_ptID[i]], X[BoundaryPolygon_ptID[0]]]
            y = [Y[BoundaryPolygon_ptID[i]], Y[BoundaryPolygon_ptID[0]]]
        else:
            x = [X[BoundaryPolygon_ptID[i]], X[BoundaryPolygon_ptID[i+1]]]
            y = [Y[BoundaryPolygon_ptID[i]], Y[BoundaryPolygon_ptID[i+1]]]
        if(PointID[BoundaryPolygon_ptID[i]] == 201 or PointID[BoundaryPolygon_ptID[i]] == 101):
            linecolor = colors[0]
        elif(PointID[BoundaryPolygon_ptID[i]] == 203 or PointID[BoundaryPolygon_ptID[i]] == 103):
            linecolor = colors[1]
        else:
            linecolor = colors[2]
        ax.plot(x, y, c=linecolor, linewidth=2)
    inlet = ax.Rectangle((0, 0), 0, 0, fc=colors[0], lw=0, alpha=1)
    sidewalls = ax.Rectangle((0, 0), 0, 0, fc=colors[2], lw=0, alpha=1)
    outlet = ax.Rectangle((0, 0), 0, 0, fc=colors[1], lw=0, alpha=1)
    return [inlet, outlet, sidewalls], ['Bottom', 'Top', 'Sides\nImpermeable\nInsulating']


def plot_mesh(X, Y, triangles, PhaseID, ax, colors='none', linewidth=0.1, xlabel='Distance(m)', ylabel='Depth(m)', mask=[]):
    PhaseID_unique = np.unique(PhaseID)
    h_mesh = []
    if(colors == 'none'):
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
                  '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    for i in range(0, len(PhaseID_unique)):
        ind = PhaseID == PhaseID_unique[i]
        if(mask != []):
            ax.triplot(X, Y, triangles[ind, :], '-', mask=mask[ind],
                       linewidth=linewidth, c=colors[i % len(colors)])
        else:
            ax.triplot(X, Y, triangles[ind, :], '-',
                       linewidth=linewidth, c=colors[i % len(colors)])
    #         handle_mesh = plt.Rectangle((0, 0), 0, 0, fc=colors[i], lw=0, alpha=1)
        handle_mesh = ax.axhline(
            y=0, xmin=0, xmax=0, color=colors[i % len(colors)], linewidth=3)
        h_mesh.append(handle_mesh)
    # ax.xlabel(xlabel)
    # ax.ylabel(ylabel)
    # ax.xlim(X.min(), X.max())
    # ax.ylim(Y.min(), Y.max())
    return h_mesh


# import matplotlib.pyplot as plt
# 绘制热液系统MATLAB程序导出的温度场等
def plot_VAR(plot, ax, X, Y, triangles, var, n_level_surf=50, vmin='', vmax='', cmp0='rainbow',
             cmap_under='k', cmap_over='w', num_ticks_cb=5, plot_cb=True, alpha=1,
             contour=True, levels_c=[], color_contour='k', linewidth_contour=1, clabels=[],
             fmt_cb='%.0f', label_cb='', extend='neither', mask=[], zorder=10):
    #     contourf\
    # extend = 'neither'
    cmap_surf = cm.get_cmap(name=cmp0, lut=None)
    if(vmin == ''):
        vmin = var.min()
    else:
        cmap_surf.set_under(cmap_under)
        # extend = 'min'
    if(vmax == ''):
        vmax = (1+1E-15)*var.max()  # 以防最小值和最大值相等而出错
        if(vmax <= vmin):
            vmax = vmin+1E-15
    else:
        cmap_surf.set_over(cmap_over)
        # if(extend == 'min'):
        #     # extend = 'both'
        # else:
        #     extend = 'max'
    if (n_level_surf == ''):
        if(mask == []):
            CS = ax.tricontourf(X, Y, triangles, var,
                                cmap=cmap_surf, extend=extend, alpha=alpha, zorder=zorder)
        else:
            CS = ax.tricontourf(X, Y, triangles, var,
                                cmap=cmap_surf, extend=extend, alpha=alpha, mask=mask, zorder=zorder)
    else:
        levels_surf = np.linspace(vmin, vmax, n_level_surf)
        # print(levels_surf)
        # levels_surf[1] = vmin+(vmax-vmin)/4*3
        # print(levels_surf, '\n')
        if(mask == []):
            CS = ax.tricontourf(X, Y, triangles, var,
                                levels=levels_surf, cmap=cmap_surf, extend=extend, alpha=alpha, zorder=zorder)
        else:
            CS = ax.tricontourf(X, Y, triangles, var,
                                levels=levels_surf, cmap=cmap_surf, extend=extend, alpha=alpha, mask=mask, zorder=zorder)
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
    cb = []
    if(plot_cb == True):
        ticks = np.linspace(vmin, vmax, num_ticks_cb)
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
    #     set x y lim
    # plot.xlim(X.min(), X.max())
    # plot.ylim(Y.min(), Y.max())
    return CS, cb


# plot chimney


def plot_Chimney(plot, ax, X, Y, triangles, var,
                 n_level_surf=50, vmin='', vmax='', cmp0='rainbow',
                 cmap_under='k', cmap_over='w',
                 contour=True, levels_c=[], color_contour='k',
                 linewidth_contour=1, clabels=[], fmt_cb='%.0f', label_cb='',
                 cb_shrink=1, cb_pad=0.01, cb_orientation='vertical', alpha=1, extend='neither'):
    #     contourf\
    # extend = 'neither'
    cmap_surf = cm.get_cmap(name=cmp0, lut=None)
    if(vmin == ''):
        vmin = var.min()
    else:
        cmap_surf.set_under(cmap_under)
        # extend = 'min'
    if(vmax == ''):
        vmax = var.max()
    else:
        cmap_surf.set_over(cmap_over)
        # if(extend == 'min'):
        #     extend = 'both'
        # else:
        #     extend = 'max'
    levels_surf = np.linspace(vmin, vmax, n_level_surf)
    mask = np.zeros_like(triangles[:, 0], dtype=bool)
    for i in range(0, len(triangles)):
        if((var[triangles[i][0]] < vmin) and (var[triangles[i][1]] < vmin) and (var[triangles[i][2]] < vmin)):
            mask[i] = True
        else:
            mask[i] = False
    MESH_tri = mtri.Triangulation(X, Y, triangles)
    MESH_tri.set_mask(mask)
    CS = ax.tricontourf(MESH_tri, var,
                        levels=levels_surf, cmap=cmap_surf, extend=extend,
                        alpha=alpha)
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
    # ticks = np.linspace(vmin, vmax, n_level_surf)
    # d_ticks = ticks[1]-ticks[0]
    # ind_del = ticks > vmax
    # for i in range(0, len(levels_c)):  # find which values near the levels_c
    #     dif = np.abs(ticks-levels_c[i])
    #     ind_del = ind_del | (dif < d_ticks/3)
    # ind_del = np.where(ind_del == True)
    # ticks = np.delete(ticks, ind_del)   # delete the near values
    # ticks = np.append(ticks, levels_c)
    # ticks = np.sort(ticks)
    #     location
    # cb = plot.colorbar(CS, format=fmt_cb,
    #                    orientation=cb_orientation, shrink=cb_shrink, pad=cb_pad, ticks=ticks)
    # if(len(levels_c) > 0):
    #     cb.add_lines(Contour)
    # cb.set_label(label_cb)
    # cb.solids.set_edgecolor("face")
    # cb.solids.set_linewidth(0.)
    #     set colorbar near figure
    #     ax.set_aspect('auto')
    #     #     set x y lim
    #     plot.xlim(X.min(), X.max())
    #     plot.ylim(Y.min(), Y.max())
    return CS


# plot stream lines
def streamlines(plt, ax, path_X, path_Z, linewidth=0.1, linecolor='gray', num_arrows=2,
                arrow_width=5, num_points_limit=10, alpha_lines=0.5):
    """
    path_X, path_Z: m x n matrix, n stream lines and m points in each line
    num_arrows: how many arrows in each line
    """
    num_lines = path_X.shape[1]
    for i in range(0, num_lines):
        # remove duplicate points
        x = path_X[:, i]
        z = path_Z[:, i]
        ind_x = path_X[1:-1, i]-path_X[0:-2, i]
        ind_z = path_Z[1:-1, i]-path_Z[0:-2, i]
        ind = ((ind_x != 0) & (ind_z != 0))
        x = path_X[0:-2, i]
        z = path_Z[0:-2, i]
        x = x[ind]
        z = z[ind]
        tmp_index = 0
        if(len(x) > num_points_limit):
            tmp_index = tmp_index+1
            # calculate length of streamlines
            dis1 = np.sqrt((x[0:-1]-x[1:])**2+(z[0:-1]-z[1:])**2)
            dis2 = dis1*0
            dis2[0] = dis1[0]
            x = x[0:-1]
            z = z[0:-1]
            for j in range(1, len(dis1)):
                dis2[j] = dis2[j-1]+dis1[j]
            ax.plot(x, z, linewidth=linewidth,
                    color=linecolor, alpha=alpha_lines)
            for k in range(0, num_arrows):
                ind = dis2 < (dis2[-1]/(num_arrows+1)*(k+1))
                xx = x[ind]
                zz = z[ind]
                x1 = xx[-2]
                z1 = zz[-2]
                x2 = xx[-1]
                z2 = zz[-1]
                dx = x2-x1
                dz = z2-z1
                arrow_width = arrow_width
                ax.arrow(x1, z1, -dx, -dz, shape='full', lw=0, length_includes_head=True,
                         head_width=arrow_width, overhang=0.3, color=linecolor, alpha=alpha_lines)
        # print('stream lines: ', tmp_index)
