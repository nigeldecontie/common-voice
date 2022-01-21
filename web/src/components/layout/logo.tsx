import * as React from 'react';
import { LocaleLink } from '../locale-helpers';

const Logo = (props: { reverse?: boolean }) => {
  const imgSrc = props.reverse
    ? require('./wmms-blk.svg')
    : require('./wmms-blk.svg');

  return (
    <LocaleLink className="main-logo" to="">
      <img
        className="main-mozilla-logo"
        src={imgSrc}
        alt="Mozilla Common Voice"
      />
    </LocaleLink>
  );
};

export default Logo;
