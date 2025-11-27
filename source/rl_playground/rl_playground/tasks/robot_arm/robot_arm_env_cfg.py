# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

import math

from isaaclab.utils import configclass

import isaaclab_tasks.manager_based.manipulation.reach.mdp as mdp
from isaaclab_tasks.manager_based.manipulation.reach.reach_env_cfg import ReachEnvCfg

##
# Pre-defined configs
##
import sys
import os

# Get the path to the current file's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the parent directory (or specific folder) to sys.path
# This allows Python to "see" the siblings
sys.path.append(os.path.join(current_dir, 'robot'))

from me6 import ME6_CFG
# from isaaclab_assets import FRANKA_PANDA_CFG  # isort: skip


##
# Environment configuration
##


@configclass
class ME6ReachEnvCfg(ReachEnvCfg):
    def __post_init__(self):
        # post init of parent
        super().__post_init__()

        # switch robot to franka
        self.scene.robot = ME6_CFG

        # override rewards
        self.rewards.end_effector_position_tracking.params["asset_cfg"].body_names = ["Link6"]
        self.rewards.end_effector_position_tracking_fine_grained.params["asset_cfg"].body_names = ["Link6"]
        self.rewards.end_effector_orientation_tracking.params["asset_cfg"].body_names = ["Link6"]

        # override actions
        self.actions.arm_action = mdp.JointPositionActionCfg(
            asset_name="robot", joint_names=["panda_joint.*"], scale=0.5, use_default_offset=True
        )

        # override command generator body
        # end-effector is along z-direction
        self.commands.ee_pose.body_name = "Link6"
        self.commands.ee_pose.ranges.pitch = (math.pi, math.pi)


@configclass
class Me6ReachEnvCfg_PLAY(ME6ReachEnvCfg):
    def __post_init__(self):
        # post init of parent
        super().__post_init__()
        # make a smaller scene for play
        self.scene.num_envs = 50
        self.scene.env_spacing = 2.5
        # disable randomization for play
        self.observations.policy.enable_corruption = False
