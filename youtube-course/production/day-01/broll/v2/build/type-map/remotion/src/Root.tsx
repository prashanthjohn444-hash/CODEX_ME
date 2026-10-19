import React from 'react';
import {Composition} from 'remotion';
import {Broll} from './Broll';
import scene from './scene.json';

export const Root: React.FC = () => (
  <Composition
    id="Broll"
    component={Broll}
    fps={scene.fps}
    width={1920}
    height={1080}
    durationInFrames={Math.round((scene.duration + scene.hold) * scene.fps)}
  />
);
