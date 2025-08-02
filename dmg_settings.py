"""
DMG build settings for SubRenamer
"""

import os

# DMG settings
settings = {
    'filename': 'SubRenamer-1.0.0.dmg',
    'volume_name': 'SubRenamer',
    'format': 'UDBZ',
    'size': '100M',
    'files': ['dist/SubRenamer.app'],
    'symlinks': {'Applications': '/Applications'},
    'icon_locations': {
        'SubRenamer.app': (100, 100),
        'Applications': (300, 100),
    },
    'background': None,  # Optional: add a background image
    'window_rect': ((100, 100), (400, 200)),
    'default_view': 'icon-view',
    'show_status_bar': False,
    'show_tab_view': False,
    'show_toolbar': False,
    'show_pathbar': False,
    'show_sidebar': False,
    'sidebar_width': 180,
    'arrange_by': None,
    'grid_offset': (0, 0),
    'grid_spacing': 100,
    'scroll_position': (0, 0),
    'label_pos': 'bottom',
    'text_size': 16,
    'icon_size': 128,
}