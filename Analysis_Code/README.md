# Analysis_Code

# Set-up of files and selections
create_file_list.py will return the relevant files for signal grid points and different background categories.

selection_criteria.py will return the list of cuts which one is testing and common region definition for Signal Region and Control Region.

Note that the two scripts above are referenced in all of the following codes.

# 1D and 2D variable distribution plots
quick_draw.py will use the simplest TTree.Draw() to quickly draw the relevant branches in certain regions.

slow_draw.py will loop through the events and calculate new variables.

draw_2D.py will draw the 2D distributions. 

# Cutflow and Yield
make_cutlow_table.py will create the cutflow table.
yield_table_create.py will create the yield table.



