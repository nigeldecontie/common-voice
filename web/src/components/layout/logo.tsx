import * as React from 'react';
import { LocaleLink } from '../locale-helpers';

export default (props: { reverse?: boolean }) => {
  const imgSrc = props.reverse
    ? require('/img/ILT CommonVoice.svg')
    : require('/img/ILT CommonVoice.svg');

  return (
    <LocaleLink className="main-logo" to="">
      <img className="main-mozilla-logo" src={imgSrc} />
    </LocaleLink>
  );
};
