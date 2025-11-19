import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

def line_plots_separate(df, 
			   valname, 
			   configs={"NROWS": 11, "NCOLS": 3, 
						"FONT_SIZE": 20, "FIGSIZE": (40, 100)},
			   show=True):
	
	# pivot_longer (wide -> long)
	df_long = pd.melt(df, id_vars=["Region"], var_name="Year",
					  value_name=valname)
	df_long.sort_values(by="Year", inplace=True)
	
	# get aggregate national quantity
	national_agg = df_long.groupby("Year").agg({valname: "sum"})
	national_agg.reset_index(inplace=True)
	
	# some configs
	FONT_SIZE = configs["FONT_SIZE"]
	NROWS = configs["NROWS"]
	NCOLS = configs["NCOLS"]
	FIGSIZE = configs["FIGSIZE"]
	
	# human friendly name
	fig_label = valname.replace("_", " ")
	
	# unique regions
	regions = df_long["Region"].unique()
	
	# set up plots
	fig, axes = plt.subplots(nrows=NROWS, ncols=NCOLS, figsize=FIGSIZE, sharey=True)
	axes = axes.flatten()

	#for i, region in enumerate(regions):
	for i in range(NROWS * NCOLS):
		ax = axes[i]

		# hide the unplotted/out of bound axes
		if i >= len(regions):
			ax.set_visible(False)
			continue
		region = regions[i]
		subset = df_long[df_long.Region == region]
		ax.plot(subset["Year"].values, subset[valname].values, 
				label=f"{region} {fig_label}")
		ax.plot(national_agg["Year"].values, 
				national_agg[valname].values, 
				label=f"Aggregate National {fig_label}")
		ax.set_yscale("log")
		ax.set_title(label=f"{fig_label} per year for {region}", fontsize=FONT_SIZE)
		ax.legend(loc="upper left", fontsize=FONT_SIZE)
		ax.tick_params(axis='both', which='major', labelsize=15)

	fig.tight_layout()
	
	if show:
		plt.show()
	return fig
	
def line_plots(df, valname, title, exceptions,
			   configs={"FONT_SIZE": 20, "FIGSIZE": (12, 12)},
			   show=False):
	
	# pivot_longer (wide -> long)
	df_long = pd.melt(df, id_vars=["Region"], var_name="Year",
					  value_name=valname)
	df_long.sort_values(by="Year", inplace=True)

	# get aggregate national quantity
	national_agg = df_long.groupby("Year").agg({valname: "sum"})
	national_agg.reset_index(inplace=True)

	# some configs
	FONT_SIZE = configs["FONT_SIZE"]
	FIGSIZE = configs["FIGSIZE"]

	# unique regions
	regions = df_long["Region"].unique()

	# set up plots
	fig, ax = plt.subplots(figsize=FIGSIZE, sharey=True)

	#for i, region in enumerate(regions):
	for i, region in enumerate(regions):

		subset = df_long[df_long.Region == region]		
		
		if region in exceptions.keys():
			ax.plot(subset["Year"].values, subset[valname].values, 
					label=f"{region}",
					marker="o", color=exceptions[region], linewidth=2)
		else:
			ax.plot(subset["Year"].values, subset[valname].values, 
					label=f"{region}",
					color="grey", linewidth=0.5, alpha=0.7)
	
	# ax.plot(national_agg["Year"].values, 
	#             national_agg[valname].values, 
	#             label=f"Aggregate National {fig_label}")
	# ax.set_yscale("log")
	ax.legend(loc="upper left", fontsize=FONT_SIZE)
	ax.set_title(label=title, fontsize=FONT_SIZE)
	ax.tick_params(axis='both', which='major', labelsize=15)
	ax.grid(True)
	fig.tight_layout()

	if show:
		plt.show()
	return fig
	
	
def heatmap(df, title, show=False):
	df_hm = df.set_index("Region")
	df_hm.sort_index(axis=1, inplace=True)

	plt.figure(figsize=(10, 10))
	ax = sns.heatmap(df_hm, cmap='YlGnBu', 
				fmt="d", linewidths=0.5)
	plt.title(title)
	plt.xlabel('Year')
	plt.ylabel('Region')
	ax.tick_params(axis='x', labelrotation=45)
	if show:
		plt.show()
	return ax


def diverge_barplot(pos, neg, title):
	# Create a diverging bar plot
	fig, ax = plt.subplots(figsize=(8, 6))

	# Plotting positive values
	ax.barh(pos.index, pos, color='blue', label='Positive', alpha=0.7)

	# Plotting negative values
	ax.barh(neg.index, neg, color='red', label='Negative', alpha=0.7)

	# Add a vertical line at 0
	ax.axvline(x=0, color='black', linestyle='--')

	# Adding labels and title
	ax.set_xlabel('Slope value')
	ax.set_ylabel('Categories')
	ax.set_title(title)
	ax.legend()


def plotly_linechart(x_series, y_series, col):
	
	from plotly.offline import init_notebook_mode, iplot

	init_notebook_mode(connected=True)         # initiate notebook for offline plot

	fig = go.Figure()

	np.random.seed(17)
	for idx, region in enumerate(wage_long[col].unique()):
		
		my_color = str(np.random.randint(0, high = 256))+','+ \
					str(np.random.randint(0, high = 256))+','+ \
					str(np.random.randint(0, high = 256))
		opacity = 1 #if idx == 1 else 0.1

		df_filter = wage_long.query(f"{col} == '{region}'")
		fig.add_trace(
			go.Scatter(
				x=list(x),
				y=list(y),
				name = f"{region}",
				mode = "lines",
				line = {
					"color": f'rgba({my_color}, {opacity})'
				},
				showlegend=True,
				visible = True
			)
		)
	fig.update_layout(
		showlegend=True,
		legend_itemclick ="toggleothers",
		legend_itemdoubleclick = "toggleothers",
		legend_title = f"{col} (Click on the legend to isolate the line)"
	)


	iplot(fig)