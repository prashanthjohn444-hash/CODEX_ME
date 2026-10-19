import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import scene from './scene.json';
import {SceneView} from './SceneView';

export const Broll: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return (
    <AbsoluteFill style={{background: '#050609'}}>
      <SceneView scene={scene} t={frame / fps} />
    </AbsoluteFill>
  );
};
